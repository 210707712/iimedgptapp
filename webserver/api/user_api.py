from flask import request, Blueprint
from server import sqltestserver
user_api = Blueprint('user_api', __name__)
@user_api.route('/test')
def test():
    return "这是测试文件"
@user_api.route('/user_login',methods=['GET', 'POST'])
def sqltest():
    data = request.json
    print(data)
    result = sqltestserver.user_login(data)
    return result
@user_api.route("/user_register", methods=['POST'])
def register():
    data = request.json
    print(data)
    result = sqltestserver.user_register(data)
    return result