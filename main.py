from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config) # config 에서 가져온 파일을 사용합니다.

    db.init_app(app) # SQLAlchemy 객체를 app 객체와 이어줍니다.
    Migrate().init_app(app, db)

    from views import main_view, store_detail_view
    from models import models
    app.register_blueprint(main_view.bp)
    app.register_blueprint(store_detail_view.bp)

    app.secret_key = "seeeeeeeeeeeecret"
    app.config['SESSION_TYPE'] = 'filesystem'

    '''
    세션을 사용하기 위해선, 보안을 위해 세션을 암호화해야 합니다.

    암호화 하는 과정에서 사용하는 비밀 키가 app.secret_key 입니다.

    따라서, 실제 서버를 사용하기 위해선 github 같은 곳에 secret_key를 절대!!! 올려선 안 됩니다.
    이후 여러분들이 서버를 실제 배포 (Apache나 Nginx)를 사용할 때는 파일을 분리하거나, 환경 변수를 설정하는 방식으로
    secret_key가 절대 깃에 노출되지 않도록 해야 합니다.

    그렇다면 SESSION_TYPE = 'filesystem'은 무슨 역할일까요?
    
    세션 정보를 별도의 파일로 뺄 수도 있고, DB에 저장할 수도 있습니다. (flask 에서는 sqlalchemy, redis/mongodb 같은 설정이 가능합니다.)
    그런데 세션을 DB로 관리하기 위해선, 별도의 구조를 만들어야겠죠?
    현재 상황에선 그런 부분을 피하기 위해 filesystem으로 관리합니다.
    '''
    
    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=3333)