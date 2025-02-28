from tools.mysqlconntool import mysqlconn
import json

def create_talk(userid, talkhistory):
    sql = "INSERT INTO talk_history (userid, talkhistory, talktime) VALUES (%s, %s, CONVERT_TZ(NOW(), '+00:00', '+08:00'))"
    val = (userid, json.dumps(talkhistory))
    # 执行插入并获取新插入的 ID
    new_id = mysqlconn.sql_updatenew(sql, val)
    return new_id

def get_talk_list(userid):
    sql = "SELECT talkid, userid, talkhistory, CONVERT_TZ(talktime, '+00:00', '+08:00') as talktime FROM talk_history WHERE userid = %s ORDER BY talktime DESC"
    val = (userid,)
    results = mysqlconn.sql_select(sql, val)
    # 将所有结果转换为字典列表
    talks = []
    for row in results:
        talk = {
            'talkid': row[0],
            'userid': row[1],
            'talkhistory': row[2],
            'talktime': row[3]
        }
        talks.append(talk)
    return talks

def get_talk_by_id(talkid, userid):
    sql = "SELECT talkid, userid, talkhistory, CONVERT_TZ(talktime, '+00:00', '+08:00') as talktime FROM talk_history WHERE talkid = %s AND userid = %s"
    val = (talkid, userid)
    result = mysqlconn.sql_select(sql, val)
    if result:
        # 将元组转换为字典
        talk = {
            'talkid': result[0][0],  # 假设talkid是第一列
            'userid': result[0][1],  # 假设userid是第二列
            'talkhistory': result[0][2],  # 假设talkhistory是第三列
            'talktime': result[0][3]  # 假设talktime是第四列
        }
        return talk
    return None

def update_talk(talkid, userid, talkhistory):
    sql = "UPDATE talk_history SET talkhistory = %s, talktime = CONVERT_TZ(NOW(), '+00:00', '+08:00') WHERE talkid = %s AND userid = %s"
    val = (json.dumps(talkhistory), talkid, userid)
    return mysqlconn.sql_update(sql, val)

def delete_talk(talkid, userid):
    sql = "DELETE FROM talk_history WHERE talkid = %s AND userid = %s"
    val = (talkid, userid)
    return mysqlconn.sql_update(sql, val) 