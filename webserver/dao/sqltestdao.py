from webserver.tools.mysqlconntool import mysqlconn
def user_login(username, password):
    sql = 'SELECT * FROM usertest WHERE username = %s AND password = %s'
    val = (username, password)
    result = mysqlconn.sql_select(sql, val)
    if len(result) == 0:
        return False
    else:
        return result
def user_register(username, password):
    sql = "INSERT INTO usertest (username, password) VALUES (%s, %s)"
    val = (username, password)
    return mysqlconn.sql_update(sql, val)
def user_isexist(username):
    sql = "SELECT * FROM usertest WHERE username = %s"
    val = (username,)
    result = mysqlconn.sql_select(sql, val)
    if len(result) == 0:
        return False
    else:
        return True