import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import zip_longest
from typing import Dict, Any, List
from rich.console import Console

from memoryscope.constants.common_constants import WORKFLOW_NAME
from memoryscope.core.memoryscope_context import MemoryscopeContext
from memoryscope.core.utils.logger import Logger
from memoryscope.core.utils.timer import Timer
from memoryscope.core.utils.tool_functions import init_instance_by_config
from memoryscope.core.worker.base_worker import BaseWorker

class BaseWorkflow(object):
    """
    工作流基类,用于管理和执行一系列工作单元(worker)。
    支持串行和并行执行工作流程,并提供上下文管理和日志记录功能。

    主要功能:
    1. 解析工作流字符串,构建执行计划
    2. 初始化和管理worker实例
    3. 执行工作流,支持串行和并行执行
    4. 提供工作流上下文管理
    5. 提供日志和控制台输出
    """

    def __init__(self,
                 name: str,
                 memoryscope_context: MemoryscopeContext,
                 workflow: str = "",
                 **kwargs):
        """
        初始化工作流实例

        Args:
            name (str): 工作流名称
            memoryscope_context (MemoryscopeContext): 全局上下文对象
            workflow (str): 工作流定义字符串,如 "[task1,task2|task3],task4"
            **kwargs: 额外的关键字参数
        """
        # 基本属性设置
        self.name: str = name
        self.memoryscope_context: MemoryscopeContext = memoryscope_context
        self.thread_pool: ThreadPoolExecutor = self.memoryscope_context.thread_pool
        self.workflow: str = workflow
        self.kwargs = kwargs

        # 工作流相关数据结构
        self.workflow_worker_list: List[List[List[str]]] = []  # 存储解析后的工作流执行计划
        self.worker_dict: Dict[str, BaseWorker | bool] = {}    # 存储worker实例或多线程标记
        self.workflow_context: Dict[str, Any] = {}             # 工作流上下文
        self.context_lock = threading.Lock()                    # 上下文锁,用于多线程同步

        # 日志记录器
        self.logger: Logger = Logger.get_logger("workflow")

        # 如果提供了工作流定义,则解析并打印
        if self.workflow:
            self.workflow_worker_list = self._parse_workflow()
            self._print_workflow()

    def workflow_print_console(self, *args, **kwargs):
        """
        控制台打印工作流信息,仅在启用动态打印时生效
        """
        if self.memoryscope_context.print_workflow_dynamic:
            Console().print(*args, **kwargs)
        return

    def _parse_workflow(self):
        """
        解析工作流字符串,配置worker线程并组织执行顺序

        工作流字符串格式支持复杂配置和可选的多线程指示。
        例如: `[task1,task2|task3],task4` 表示task1和task2可以与task3并行执行,然后执行task4

        Returns:
            List[List[List[str]]]: 表示执行计划的嵌套列表,包含并行组和任务
        """
        # 匹配工作流组件的正则表达式
        pattern = r"(\[[^\]]*\]|[^,]+)"
        workflow_split = re.findall(pattern, self.workflow)

        for workflow_part in workflow_split:
            # 处理如 [d,e,f|g,h] 格式的工作流部分
            workflow_part = workflow_part.strip()
            if '[' in workflow_part or ']' in workflow_part:
                workflow_part = workflow_part.replace('[', '').replace(']', '')

            # 按 | 分割识别潜在的并行任务组
            line_split = [x.strip() for x in workflow_part.split("|") if x]

            if len(line_split) <= 0:
                continue

            # 根据组数确定是否涉及多线程
            is_multi_thread: bool = len(line_split) > 1

            # 处理如 ["d","e","f"] 的子任务列表
            line_split_split: List[List[str]] = []
            for sub_line_split in line_split:
                sub_split = [x.strip() for x in sub_line_split.split(",")]
                line_split_split.append(sub_split)
                # 添加worker及其多线程标记
                for sub_item in sub_split:
                    self.worker_dict[sub_item] = is_multi_thread

            self.workflow_worker_list.append(line_split_split)

        return self.workflow_worker_list

    def _print_workflow(self):
        """
        以结构化格式打印工作流阶段
        每个工作流阶段都会详细显示其组成部分,可以是单个元素或由 ' | ' 分隔的分组元素
        """
        self.logger.info(f"----- workflow.{self.name}.print.begin -----")
        i: int = 0
        for workflow_part in self.workflow_worker_list:
            if len(workflow_part) == 1:
                # 处理单元素工作流部分
                for w in workflow_part[0]:
                    self.logger.info(f"stage{i}: {w}")
                    i += 1
            else:
                # 处理多并行元素工作流部分
                for w_zip in zip_longest(*workflow_part, fillvalue="-"):
                    self.logger.info(f"stage{i}: {' | '.join(w_zip)}")
                    i += 1
                    # 跳过zip_longest中用于填充的占位符
                    for w in w_zip:
                        if w == "-":
                            continue
        self.logger.info(f"----- workflow.{self.name}.print.end -----")

    def init_workers(self, is_backend: bool = False, **kwargs):
        """
        根据配置初始化worker实例

        Args:
            is_backend (bool): 是否在后端上下文中初始化worker
            **kwargs: 初始化时传递的额外参数

        Raises:
            RuntimeError: 如果worker_dict中的worker在配置中不存在
        """
        for name in list(self.worker_dict.keys()):
            if name not in self.memoryscope_context.worker_conf_dict:
                raise RuntimeError(f"worker={name} is not exists in worker config!")

            # 所有worker共享上下文对象
            self.worker_dict[name] = init_instance_by_config(
                config=self.memoryscope_context.worker_conf_dict[name],
                name=name,
                is_multi_thread=is_backend or self.worker_dict[name],
                context=self.workflow_context,
                memoryscope_context=self.memoryscope_context,
                context_lock=self.context_lock,
                thread_pool=self.thread_pool,
                **kwargs)

    def _run_sub_workflow(self, worker_list: List[str]) -> bool:
        """
        执行子工作流

        Args:
            worker_list: 要执行的worker列表

        Returns:
            bool: 执行是否成功
        """
        for name in worker_list:
            worker = self.worker_dict[name]
            worker.run()
            if not worker.continue_run:
                self.logger.warning(f"worker={worker.name} stop workflow!")
                return False
        return True

    def run_workflow(self, **kwargs):
        """
        执行工作流,协调self.workflow_worker_list中定义的步骤
        支持基于workflow_worker_list结构的串行和并行执行子工作流

        如果工作流部分只包含单个项目,则按顺序执行
        对于包含多个项目的部分,使用线程池并行执行
        如果任何子工作流返回False,工作流将停止

        Args:
            **kwargs: 传递给上下文的额外关键字参数
        """
        with Timer(f"workflow.{self.name}", time_log_type="wrap"):
            log_buf = f"Operation: {self.name}"
            self.logger.info(log_buf)
            self.workflow_print_console(log_buf, style="bold red")
            self.workflow_context.clear()
            self.workflow_context.update({WORKFLOW_NAME: self.name, **kwargs})
            n_stage = len(self.workflow_worker_list)
            
            # 遍历工作流的每个部分
            for index, workflow_part in enumerate(self.workflow_worker_list):
                # 串行执行单项部分
                if len(workflow_part) == 1:
                    log_buf = f"\t- Operation: {self.name} | {index+1}/{n_stage}: {workflow_part[0]}"
                    self.logger.info(log_buf)
                    self.workflow_print_console(log_buf, style="bold red")
                    if not self._run_sub_workflow(workflow_part[0]):
                        break
                # 并行执行多项部分
                else:
                    t_list = []
                    # 向线程池提交任务
                    n_sub_stage = len(workflow_part)
                    for sub_index, sub_workflow in enumerate(workflow_part):
                        log_buf = f"\t- Operation: {self.name} | {index+1}/{n_stage} | sub workflow {sub_index+1}/{n_sub_stage}: {str(sub_workflow)}"
                        self.logger.info(log_buf)
                        self.workflow_print_console(log_buf, style="red")
                        t_list.append(self.thread_pool.submit(self._run_sub_workflow, sub_workflow))

                    # 检查结果,如果任何任务返回False,停止工作流
                    flag = True
                    for future in as_completed(t_list):
                        if not future.result():
                            flag = False
                    if not flag:
                        break
