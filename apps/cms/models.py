from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class CMSUser(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    PwdRecord = db.relationship("PwdRecord", backref="author")
    realname = db.Column(db.String(64))  # 真实姓名
    sex = db.Column(db.String(4), default='男')
    confirmed = db.Column(db.Boolean, default=False)  # 是否保持登录
    location = db.Column(db.String(64))  # 地区
    about_me = db.Column(db.Text())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, username, password, email):
            self.username = username
            self.password = password
            self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

class PwdRecord(db.Model):
    __tablename__ = "history_pwd"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _password = db.Column(db.String(100), nullable=False)
    change_time = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

class Post(db.Model):
    """微博模型"""
    __tablename__ = 'bbs_posts'     # 数据库表名
    id = db.Column(db.Integer, primary_key=True)                                # 微博 id
    body = db.Column(db.Text)                                                   # 微博内容
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # 发布时间
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))             # 作者 id
    comments = db.relationship('Comment', backref='post', lazy='dynamic')       # 评论

    @staticmethod
    def generate_fake_posts(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = CMSUser.query.count()
        for i in range(count):
            u = CMSUser.query.offset(randint(0, user_count - 1)).first()
            p = Post(
                body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                timestamp=forgery_py.date.date(True),
                author=u
            )
            db.session.add(p)
            db.session.commit()

    def to_json(self):
        return {
            'posTime': self.timestamp,
            'post': self.body,
            'authorID': self.author_id
        }

#
class Comment(db.Model):
    """评论模型"""
    __tablename__ = 'comments'      # 数据库表名
    id = db.Column(db.Integer, primary_key=True)                                # 评论 id
    body = db.Column(db.Text)                                                   # 评论内容
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # 评论时间
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))             # 作者 id
    post_id = db.Column(db.Integer, db.ForeignKey('bbs_posts.id'))                  # 微博 id

    def to_json(self):
        return {
            'postTime': self.timestamp,
            'post': self.body,
            'postID': self.post_id,
            'authorID': self.author_id
        }

class MarxQuestionBank(db.Model):
    __tablename__ = "Marx"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(300))
    answer = db.Column(db.String(200))
    options = db.Column(db.String(300))
