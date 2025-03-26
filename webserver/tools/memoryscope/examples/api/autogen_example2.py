from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import Optional, List, Dict, Tuple
from autogen import ConversableAgent, Agent

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
        
        # 本地模型路径
        self.model_path = "/home/user/gptdata/fcg/model/Qwen/Qwen2___5-14B-Instruct"
        
        # 加载模型和分词器
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path)
    
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
        
        # 使用加载的本地模型生成回复
        inputs = self.tokenizer(query, return_tensors="pt")  # 将输入文本转化为模型输入
        outputs = self.model.generate(inputs['input_ids'], max_length=200)  # 生成文本
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)  # 解码生成的文本
        
        return True, response

# 示例启动
def main():
    assistant = MemoryScopeAgent(name="assistant")
    user_proxy = Agent(name="user")
    assistant.initiate_chat(user_proxy, message="有什么需要帮忙的吗？")

if __name__ == "__main__":
    main()
