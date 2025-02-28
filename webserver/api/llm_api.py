from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from flask import request, Blueprint, Response, json
from server import llm_server
from dao import llm_dao

llm_api = Blueprint('llm_api', __name__)

@llm_api.route('/llm/request',methods=['GET', 'POST'])
def stream_numbers():
    data = request.json
    query = data['query']
    prompt = data['prompt']
    userid = data['userid']
    talkid = data.get('talkid')
    
    if not prompt:
        prompt = "你是一名医疗专业人员,请回答用户的问题"

    def chat():
        messages = []
        new_talk_id = None

        if talkid:
            talk = llm_dao.get_talk_by_id(talkid, userid)
            if talk and talk['talkhistory']:
                messages = json.loads(talk['talkhistory'])

        messages.append({'role': 'system', 'content': prompt})
        messages.append({'role': Role.USER, 'content': query})

        whole_message = ''
        responses = Generation.call(Generation.Models.qwen_turbo, messages=messages,
                                    api_key="sk-f99e8af9f60c420da59b177d8f186a53", result_format='message', stream=True,
                                    incremental_output=True)

        for response in responses:
            part_message = response.output.choices[0]['message']['content']
            whole_message += part_message
            json_data = json.dumps({"message": part_message})
            yield f"data: {json_data}\n\n"

        messages.append({'role': 'assistant', 'content': whole_message})

        if talkid:
            llm_dao.update_talk(talkid, userid, messages)
        else:
            new_talk_id = llm_dao.create_talk(userid, messages)
            # 发送新的 talkid 给前端
            json_data = json.dumps({"message": "done", "talkid": new_talk_id}, ensure_ascii=False)
            yield f"data: {json_data}\n\n"
            return

        json_data = json.dumps({"message": "done"}, ensure_ascii=False)
        yield f"data: {json_data}\n\n"

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)
@llm_api.route('/llm/talk/create', methods=['POST'])
def create_talk():
    data = request.json
    return llm_server.create_talk(data)

@llm_api.route('/llm/talk/list', methods=['POST'])
def get_talk_list():
    data = request.json
    return llm_server.get_talk_list(data)

@llm_api.route('/llm/talk/get', methods=['POST'])
def get_talk():
    data = request.json
    return llm_server.get_talk_by_id(data)

@llm_api.route('/llm/talk/update', methods=['POST'])
def update_talk():
    data = request.json
    return llm_server.update_talk(data)

@llm_api.route('/llm/talk/delete', methods=['POST'])
def delete_talk():
    data = request.json
    return llm_server.delete_talk(data)