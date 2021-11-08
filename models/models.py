from app import db

'''
model.py
이 파일은 데이터베이스의 제약 조건을 명시하는 파일입니다.
관계형 데이터베이스의 데이터를 객체랑 연결 시켜주는 것을 ORM (Object Relational Mapping) 이라고 불러요.
즉, 이 파일은 외부에 존재하는 DB를 서버에서 사용하기 위해, DB와 동일한 제약조건을 객체에 걸어버리는 겁니다.
'''

class rabbitUser(db.Model):

    __tablename__ = 'rabbitUser' # 테이블 이름입니다. 객체 이름과 달라도 되지만, 외부 테이블의 이름이 되기 때문에 유의해서 설정하세요.

    id          = db.Column(db.String(20), primary_key=True, nullable=False) 
    password    = db.Column(db.String(255), nullable=False)
    nickname    = db.Column(db.String(20))
    point       = db.Column(db.Integer)
    address     = db.Column(db.String(255))
    telephone   = db.Column(db.String(11))
    rank        = db.Column(db.Integer)

    def __init__(self, id, password, nickname, telephone):
        self.id         = id
        self.password   = password
        self.nickname   = nickname
        self.telephone  = telephone
        self.point      = 0
        self.rank       = 0


class rabbitStore(db.Model):
    
    __tablename__ = 'rabbitStore'
    
    id          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name        = db.Column(db.String(20), nullable=False)
    location    = db.Column(db.String(50))
    rating      = db.Column(db.Integer)
    open_time   = db.Column(db.String(5))
    close_time  = db.Column(db.String(5))
    stars       = db.Column(db.Integer)
    thumbnail   = db.Column(db.String(255))


class rabbitMenu(db.Model):

    __tablename__ = 'rabbitMenu'

    id          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    food_name   = db.Column(db.String(20), nullable=False)
    store_id    = db.Column(db.Integer, db.ForeignKey('rabbitStore.id')) # 외부키를 사용할 때는 '테이블 이름.속성' 을 사용해야 합니다. 객체 이름이 아니에요!
    description = db.Column(db.String(255))
    price       = db.Column(db.Integer, nullable=False)
    thumbnail   = db.Column(db.String(255))


class rabbitReview(db.Model):

    __tablename__ = 'rabbitReview'

    id          = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('rabbitUser.id'), nullable=False)
    store_id    = db.Column(db.Integer, db.ForeignKey('rabbitStore.id'), nullable=False)
    rating      = db.Column(db.Float)
    content     = db.Column(db.Text())