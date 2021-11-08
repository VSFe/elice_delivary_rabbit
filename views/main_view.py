'''
view는 우리 눈에 보이는 부분을 관리합니다.

지난 시간에 작업했을 때는 view를 여러 파일로 분리하지 않았는데, 상황에 따라 파일을 분리할 수 있습니다.
그러면 어떻게 관리하냐고요?

어차피 각 파일마다 별도의 Blueprint를 만들테니, __init__.py에서 전부 import 하고
각각 다 register_blueprint를 활용해서 이어줍니다.

추가로, 코드를 보다보면 query를 사용한 것이 많은데, 이를 활용하면 SQL 구문을 직접 사용하지 않고
ORM을 통해 간접적으로 db에 작업 명령을 내릴 수 있습니다.
'''

from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from models.models import *
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    store_list = rabbitStore.query.order_by(rabbitStore.name.asc())
    return render_template('main.html', store_list=store_list)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # 회원가입 과정을 거쳐야겠다!
        # 만약에 같은 아이디가 있으면 어떡해?
        username  = request.form['user_id']
        password  = request.form['password']
        nickname  = request.form['nickname']
        telephone = request.form['telephone']

        user = rabbitUser.query.filter_by(id=request.form['user_id']).first()
        if not user:
            password = generate_password_hash(password)
            user = rabbitUser(id=username, password=password, nickname=nickname, telephone=telephone)
        
            db.session.add(user)
            db.session.commit()

            flash("회원가입이 완료되었습니다. 로그인 해 주세요.")
            return redirect(url_for('main.home'))
        else:
            flash("이미 가입된 아이디입니다.")
            return redirect(url_for('main.home'))

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        id          = request.form['user_id']
        password    = request.form['password']

        user_data = rabbitUser.query.filter_by(id=id).first()

        if not user_data:
            flash("없는 아이디입니다.")
            return render_template('login.html')
        if not check_password_hash(user_data.password, password):
            flash("비밀번호가 틀렸습니다.")
            return render_template('login.html')
        else:
            session.clear()
            session['user_id'] = id
            session['nickname'] = user_data.nickname

            flash(f'안녕하세요. {user_data.nickname}님!')
            return redirect(url_for('main.home'))

@bp.route('/logout')
def logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect(url_for('main.home'))