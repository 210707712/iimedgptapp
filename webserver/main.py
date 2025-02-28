import flask
from flask import request
from flask_cors import CORS
from api.test_api import test_api
from api.llm_api import llm_api
from api.appllm_api import appllm_api
from api.user_api import user_api
#  创建蓝图对象
app = flask.Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(test_api, url_prefix='/test_api')
app.register_blueprint(appllm_api, url_prefix='/appllm_api')
app.register_blueprint(llm_api, url_prefix='/llm_api')
app.register_blueprint(user_api, url_prefix='/user_api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=30006, debug=True)