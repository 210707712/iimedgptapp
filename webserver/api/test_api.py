from flask import request, Blueprint
from server import sqltestserver
test_api = Blueprint('test_api', __name__)
@test_api.route('/test')
def test():
    return "这是测试文件"
@test_api.route('/sqltestuser_login',methods=['GET', 'POST'])
def sqltest():
    data = request.json
    print(data)
    result = sqltestserver.user_login(data)
    return result
@test_api.route("/sqltestuser_register", methods=['POST'])
def register():
    data = request.json
    print(data)
    result = sqltestserver.user_register(data)
    return result