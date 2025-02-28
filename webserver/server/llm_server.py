from dao import llm_dao
import json

def create_talk(data):
    userid = data['userid']
    talkhistory = data.get('talkhistory', [])
    
    try:
        llm_dao.create_talk(userid, talkhistory)
        return {"code": 200, "message": "对话创建成功", "data": {}}
    except Exception as e:
        return {"code": 500, "message": f"创建失败：{str(e)}", "data": {}}

def get_talk_list(data):
    userid = data['userid']
    try:
        talks = llm_dao.get_talk_list(userid)
        return {"code": 200, "message": "获取成功", "data": talks}
    except Exception as e:
        return {"code": 500, "message": f"获取失败：{str(e)}", "data": []}

def get_talk_by_id(data):
    talkid = data['talkid']
    userid = data['userid']
    try:
        talk = llm_dao.get_talk_by_id(talkid, userid)
        if talk:
            return {"code": 200, "message": "获取成功", "data": talk}
        return {"code": 404, "message": "对话不存在", "data": {}}
    except Exception as e:
        return {"code": 500, "message": f"获取失败：{str(e)}", "data": {}}

def update_talk(data):
    talkid = data['talkid']
    userid = data['userid']
    talkhistory = data['talkhistory']
    
    try:
        result = llm_dao.update_talk(talkid, userid, talkhistory)
        if result:
            return {"code": 200, "message": "更新成功", "data": {}}
        return {"code": 404, "message": "对话不存在", "data": {}}
    except Exception as e:
        return {"code": 500, "message": f"更新失败：{str(e)}", "data": {}}

def delete_talk(data):
    talkid = data['talkid']
    userid = data['userid']
    
    try:
        result = llm_dao.delete_talk(talkid, userid)
        # if result:
        return {"code": 200, "message": "删除成功", "data": {}}
        # return {"code": 404, "message": "对话不存在", "data": {}}
    except Exception as e:
        return {"code": 500, "message": f"删除失败：{str(e)}", "data": {}} 