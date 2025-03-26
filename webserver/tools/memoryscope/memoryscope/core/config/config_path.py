import json
import time
import questionary
import yaml
from memoryscope import MemoryScope
from pydantic.v1 import BaseModel
import dashscope
dashscope.api_key = "sk-f99e8af9f60c420da59b177d8f186a53"

def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config

config_path = "/home/user/gptdata/fcg/memoryscope/memoryscope/core/config/demo_config_local.yaml"
ms = MemoryScope(config_path=config_path)
memory_chat = ms.default_memory_chat
memory_chat.run_service_operation("delete_all",role_name="user1")
# # response = memory_chat.chat_with_memory(query="我的爱好是吉他。",role_name="user111")
# # for _resp in response:
# #     questionary.print(_resp.delta, end="")
# # questionary.print("")
# # print("回答：\n", response.message.content)

# # print("记忆：\n", response.meta_data["memories"])
# # response = memory_chat.chat_with_memory(query="我在阿里巴巴干活",role_name="user1")
# # print("回答4：\n" + response.message.content)
# # response = memory_chat.chat_with_memory(query="今天下午吃什么水果好？")
# # print("回答5：\n" + response.message.content)
# # response = memory_chat.chat_with_memory(query="我喜欢吃西瓜。",role_name="user1")
# # print("回答6：\n" + response.message.content)
# # response = memory_chat.chat_with_memory(query="帮我写一句给朋友的生日祝福语，简短一点。")
# # print("回答7：\n" + response.message.content)
# # result = memory_chat.run_service_operation("consolidate_memory",role_name="user1")
# # print(f"consolidate_memory result={result}")

# # response = memory_chat.chat_with_memory(query="你知道我的乐器爱好是什么？")
# # print("回答2：\n", response.message.content)
# # print("记忆2：\n", response.meta_data["memories"])

response = memory_chat.chat_with_memory(query="我的爱好是吉他",role_name="user1",system_prompt="你是由中科智慧健康研究院开发的医疗人工智能助手IIMedGPT")
for _resp in response:
    questionary.print(_resp.delta, end="")
questionary.print("")
response = memory_chat.chat_with_memory(query="今天是什么日子？",role_name="user1",system_prompt="你是由中科智慧健康研究院开发的医疗人工智能助手IIMedGPT")
for _resp in response:
    questionary.print(_resp.delta, end="")
questionary.print("")

# response = memory_chat.chat_with_memory(query="我的爱好是钢琴",role_name="user1")
# for _resp in response:
#     questionary.print(_resp.delta, end="")
# questionary.print("")

result_consolidate_memory = memory_chat.run_service_operation("consolidate_memory",role_name="user1")
print(f"consolidate_memory result={result_consolidate_memory}")
if result_consolidate_memory:
    memories_count = result_consolidate_memory.count("observation") + result_consolidate_memory.count("insight")
    if memories_count > 10:
        result_reflect_and_reconsolidate = memory_chat.run_service_operation("reflect_and_reconsolidate",role_name=userid)  # 反思与再巩固
        print(result_reflect_and_reconsolidate)
# # print(type(result))
# # response = memory_chat.chat_with_memory(query="你知道我的乐器爱好是什么？",role_name="user")
# # print("回答2：\n", response.message.content)
# # print("记忆2：\n", response.meta_data["memories"])

# response = memory_chat.chat_with_memory(query="你知道我的乐器爱好是什么？",role_name="user1")
# for _resp in response:
#     questionary.print(_resp.delta, end="")
# # questionary.print("")
# print("记忆3：\n", _resp.meta_data["memories"])

# def chat(userid,query,prompt):
#     messages = []
#     whole_message = ''
#     responses =memory_chat.chat_with_memory(query=query, role_name=userid, system_prompt=prompt) 

#     for response in responses:
#         part_message = response.delta
#         whole_message += part_message
#         json_data = json.dumps({"message": part_message})
#         yield f"data: {json_data}\n\n"

        
#     messages.append({'role': 'assistant', 'content': whole_message})
    
#     json_data = json.dumps({"message": "done"}, ensure_ascii=False)
#     yield f"data: {json_data}\n\n"
    
#     result_consolidate_memory = memory_chat.run_service_operation("consolidate_memory",role_name=userid)  # 巩固记忆
#     print(result_consolidate_memory)
#     if result_consolidate_memory:
#         memories_count = result_consolidate_memory.count("observation") + result_consolidate_memory.count("insight")
#         if memories_count > 10:
#             result_reflect_and_reconsolidate = memory_chat.run_service_operation("reflect_and_reconsolidate",role_name=userid)  # 反思与再巩固
#             print(result_reflect_and_reconsolidate)
  
# time_start = time.time()
# resps = chat(userid="user1",query="我的爱好是吉他。",prompt="你是由中科智慧健康研究院开发的医疗人工智能助手IIMedGPT")
# for resp in resps:
#     print(resp)
# time_end = time.time()
# print(f"time cost: {time_end - time_start} seconds")
