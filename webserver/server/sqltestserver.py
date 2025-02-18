from webserver.dao import sqltestdao
def is_null(username, password):
    if username == '' or password == '':
        return True
    else:
        return False
def user_isexist(username):
    if sqltestdao.user_isexist(username):
        return True
    return False
def user_login(data):
    username = data['username']
    password = data['password']
    user_result = sqltestdao.user_login(username, password)
    if is_null(username, password):
        result = {"err": 1, "message": "账号或密码不能为空！", "data": {}}
    elif user_result:
        user_first = user_result[0]
        result = {"code": 20000, "err": 0, "message": "登陆成功",
                  "data": {"token": user_first[3], "userid": user_first[0]}}
    elif user_isexist(username):
        result = {"err": 2, "message": "密码错误，请输入正确密码", "data": {}}
    else:
        result = {"err": 3, "message": "不存在该用户，请先注册!", "data": {}}
    return result
def user_register(data):
    username = data['usernameInput']
    password = data['passwordInput']
    if is_null(username, password):
        result = {"err": 1, "message": "账号或密码不能为空！", "data": {}}
    elif user_isexist(username):
        result = {"err": 2, "message": "用户已存在，请直接登录", "data": {}}
    else:
        sqltestdao.user_register(username, password)
        result = {"code": 20000, "message": "注册成功！", "data": {}}
    return result