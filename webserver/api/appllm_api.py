from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
import webserver.tools.milvus.test as zhishi
from flask import request, Blueprint, Response, json
appllm_api = Blueprint('appllm_api', __name__)

# 接收全部的信息
messages = []
messages2 = []

def validate_and_reset_messages(messages):
    # 检查列表是否为空或第一个元素的role不是'system'
    if not messages or messages[0]['role'] != 'system':
        messages.clear()
        return messages

    # 获取messages中除了第一个元素以外的role列表
    actual_roles = [msg['role'] for msg in messages[1:]]

    # 检查剩余元素的role是否按'user'和'assistant'交替的顺序出现
    # 我们需要确保列表长度是奇数（因为第一个元素是'system'）
    # 并且从第二个元素开始，'user'和'assistant'交替
    if len(actual_roles) % 2 != 0 or not all(actual_roles[i] == 'user' and actual_roles[i + 1] == 'assistant' for i in range(0, len(actual_roles) - 1, 2)):
        messages.clear()

    return messages
def validate_and_reset_messages1(messages):
    # 检查列表是否为空或第一个元素的role不是'system'
    # if not messages or messages[0]['role'] != 'system':
    #     messages.clear()
    #     return messages

    # 获取messages中除了第一个元素以外的role列表
    # actual_roles = [msg['role'] for msg in messages[1:]]
    actual_roles=messages
    # 检查剩余元素的role是否按'user'和'assistant'交替的顺序出现
    # 我们需要确保列表长度是奇数（因为第一个元素是'system'）
    # 并且从第二个元素开始，'user'和'assistant'交替
    if len(actual_roles) % 2 != 0 or not all(actual_roles[i] == 'user' and actual_roles[i + 1] == 'assistant' for i in range(0, len(actual_roles) - 1, 2)):
        messages.clear()

    return messages
@appllm_api.route('/llm/request')
def stream_numbers():
    global messages
    query = request.args.get('query', default='default query')
    prompt = request.args.get('prompt')
    if not prompt:
        prompt = "你是一名医疗专业人员，遵循指令输出markdown格式文本"
    def chat():
        messages.append({'role': 'system', 'content': prompt})
        print(query)
        messages.append({'role': Role.USER, 'content': query})
        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_turbo, messages=messages,
                                    api_key="sk-f99e8af9f60c420da59b177d8f186a53", result_format='message', stream=True,
                                    incremental_output=True)

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            print(part_message, end='')
            json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
            yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        # print('结束')

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


@appllm_api.route('/llm/requestIIMedGPT')
def requestIIMedGPT():
    # messages=[]
    question = request.args.get('query', default='default query')
    prompt = request.args.get('prompt')
    if not prompt:
        prompt = "你是一名医疗专业人员，遵循指令输出markdown格式文本"
    global messages
    print(messages)
    if len(messages) >=10:
        messages.clear()
    # print(messages)
    validate_and_reset_messages(messages)
    # 检查 messages 中是否已经存在相同的 prompt
    prompt_exists = False
    for msg in messages:
        # if msg['role'] == 'system' and msg['content'] == prompt:
        if msg['role'] == 'system':
            prompt_exists = True
            break
    print(prompt_exists)
    # 如果不存在，则添加 prompt
    if not prompt_exists:
        messages.append({"role": "system", "content": prompt})
    else:
        messages[0]["content"]=prompt
    print(messages)
    messages.append({"role": "user", "content": question})
    print(messages)
    
    def chat():
        from openai import OpenAI
        import time
        whole_message = ''
        client = OpenAI(base_url='http://202.127.200.31:30016/v1',api_key="not used actually")

        response = client.chat.completions.create(
            model="IIMedGPT-34B-chat",
            messages=messages,
            max_tokens=4096,
            temperature=0.7,
            stream = True
        )
        for chunk in response:
            # print(chunk)
            if  chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                whole_message += content
                json_data = json.dumps({"message": content})
                time.sleep(0.2)
                yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
                
        messages.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    sse_headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }
    return Response(chat(), content_type='text/event-stream', headers=sse_headers)

@appllm_api.route('/llm/requestIIMedGPT2')
def requestIIMedGPT2():
    question = request.args.get('query', default='default query')
    prompt = request.args.get('prompt')
    if not prompt:
        prompt = "你是一名医疗专业人员，遵循指令输出markdown格式文本"
    global messages2
    print(messages2)
    if len(messages) >=10:
        messages.clear()
    prompt_exists = False
    print(messages2)
    messages2.append({"role": "user", "content": question})
    print(messages2)

    def chat():
        from openai import OpenAI
        import time
        whole_message = ''
        client = OpenAI(base_url='http://202.127.200.31:30016/v1',api_key="not used actually")

        response = client.chat.completions.create(
            model="IIMedGPT-32B-Qwen2.5",
            messages=messages,
            max_tokens=32000,
            temperature=0.5,
            stream = True
        )
        for chunk in response:
            # print(chunk)
            if  chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                whole_message += content
                json_data = json.dumps({"message": content})
                time.sleep(0.2)
                yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
                
        messages.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

    sse_headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }
    return Response(chat(), content_type='text/event-stream', headers=sse_headers)


@appllm_api.route('/llm/zhishi')
def requestzhishi():
    question = request.args.get('query')
    a=zhishi.query(question, 7879)
    return a
@appllm_api.route('/llm/zhishi2')
def requestzhishi2():
    question = request.args.get('query')
    a=zhishi.query(question, 7880)
    return a
@appllm_api.route('/llm/clear')
def clear():

    global messages
    print(messages)
    messages=[]
    print(messages)
    return messages
@appllm_api.route('/llm/clear2')
def clear2():

    global messages2
    print(messages2)
    messages2=[]
    print(messages2)
    return messages2
@appllm_api.route('/llm/seemessage')
def seemessage():

    global messages
    
    return messages
@appllm_api.route('/llm/seemessage2')
def seemessage2():

    global messages2
    
    return messages2

