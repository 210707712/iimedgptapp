from typing import Optional, List, Dict, Tuple
from autogen import ConversableAgent, Agent

# 自定义本地模型类
class CustomLocalModel:
    def __init__(self, model_path):
        # 自定义加载模型的方法
        self.model_path = model_path
        self.model = self.load_model(model_path)  # 通过自定义方法加载模型
    
    def load_model(self, model_path):
        # 假设你使用 PyTorch 或其他框架来加载模型
        # 这里使用伪代码表示模型加载过程
        import torch
        model = torch.load(model_path)
        return model
    
    def generate(self, query):
        # 通过模型生成回复（具体生成过程依据你的模型而定）
        # 这里使用伪代码，假设模型有一个 `generate` 方法
        response = self.model.generate(query)  
        return response

class MemoryScopeAgent(ConversableAgent):
    def __init__(
            self,
            name: str = "assistant",
            system_message: Optional[str] = "",
            human_input_mode: str = "NEVER",
            llm_config: Optional[Dict] = None,
            arguments: Optional[Dict] = None,
            **kwargs,
    ):
        super().__init__(name=name, system_message=system_message, human_input_mode=human_input_mode, **kwargs)
        
        # 使用自定义本地模型加载
        self.model = CustomLocalModel("/home/user/gptdata/fcg/model/Qwen/Qwen2___5-14B-Instruct")
    
    def generate_reply_with_memory(
            self,
            messages: Optional[List[Dict]] = None,
            sender: Optional[Agent] = None,
            config: Optional[Dict] = None,
    ) -> Tuple[bool, str]:
        # 从消息中提取查询内容
        contents = []
        for message in messages:
            if message.get("role") != self.name:
                contents.append(message.get("content", ""))
        
        query = contents[-1]
        
        # 使用自定义加载的本地模型生成回复
        response = self.model.generate(query)
        
        return True, response

# 示例启动
def main():
    assistant = MemoryScopeAgent(name="assistant")
    user_proxy = Agent(name="user")
    assistant.initiate_chat(user_proxy, message="有什么需要帮忙的吗？")

if __name__ == "__main__":
    main()
