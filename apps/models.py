from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, request
# from exts import db, login_manager
from exts import db

class Follow(db.Model):
    """关注者/被关注者模型"""
    __tablename = 'follows'     # 数据库表名
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # 用户关注的人 id
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # 用户粉丝 id
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)                       # 关注时间

# class User(UserMixin, db.Model):
#     """用户模型"""
#     __tablename__ = 'users'     # 数据库表名
#     id = db.Column(db.Integer, primary_key=True)                        # 用户 id
#     email = db.Column(db.String(64), unique=True, index=True)           # 邮箱
#     username = db.Column(db.String, unique=True, index=True)            # 用户名
#     realname = db.Column(db.String(64))                                 # 真实姓名
#     sex = db.Column(db.String, default='男')                            # 性别
#     password_hash = db.Column(db.String(128))                           # 密码哈希值
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))          # 角色 id
#     confirmed = db.Column(db.Boolean, default=False)                    # 是否保持登录
#     location = db.Column(db.String(64))                                 # 地区
#     about_me = db.Column(db.Text())                                     # 个人简介
#     member_since = db.Column(db.DateTime, default=datetime.utcnow)      # 注册时间
#     last_seen = db.Column(db.DateTime, default=datetime.utcnow)         # 最新登录时间
#     avatar_hash = db.Column(db.String(32))                              # 头像哈希值
#     posts = db.relationship('Post', backref='author', lazy='dynamic')   # 微博<关系>
#
#     # 用户关注的人<关系>
#     followed = db.relationship('Follow',
#                                foreign_keys=[Follow.follower_id],       # 在 Follow 模型中自引用
#                                backref=db.backref('follower', lazy='joined'),   # join 立即加载所有相关对象
#                                lazy='dynamic',
#                                cascade='all, delete-orphan')            # 删除所有记录
#     # 用户的粉丝<关系>
#     followers = db.relationship('Follow',
#                                 foreign_keys=[Follow.followed_id],      # 在 Follow 模型中自引用
#                                 backref=db.backref('followed', lazy='joined'),  # join 立即加载所有相关对象
#                                 lazy='dynamic',
#                                 cascade='all, delete-orphan')           # 删除所有记录
#     # 微博的评论<关系>
#     comments = db.relationship('Comment',
#                                backref='author',
#                                lazy='dynamic')
#
#     def set_follow(self, user):
#         """ 设置关注用户
#
#         :param user: 指定用户
#         """
#         if not self.is_following(user):
#             f = Follow(follower=self, followed=user)
#             db.session.add(f)
#
#     def set_unfollow(self, user):
#         """ 设置取消关注用户
#         :param user: 指定用户
#         """
#         f = self.followed.filter_by(followed_id=user.id).first()
#         if f:
#             # 从 follows 表中删除该关注关系
#             db.session.delete(f)
#
#     def is_following(self, user):
#         """ 是否关注某用户
#         :param user: 指定用户
#         :return: 已关注返回 True，反之返回 False
#         """
#         if self.followed.filter_by(followed_id=user.id).first():
#             return True
#         return False
#
#     def is_followed_by(self, user):
#         """ 是否被某用户关注
#         :param user: 指定用户
#         :return: 已关注返回 True，反之返回 False
#         """
#         if self.followers.filter_by(follower_id=user.id).first():
#             return True
#         return False
#
#     @property
#     def followed_posts(self):
#         """查询关注者微博列表，使用了联结操作，通过 user.id 链接 follow, post 两个数据表
#         :return: 关注者微博列表
#         """
#         return Post.query.join(
#             Follow, Follow.followed_id == Post.author_id).filter(
#             Follow.follower_id == self.id)
#
#     @property
#     def password(self):
#         """ 密码属性不可被访问"""
#         raise AttributeError('密码不可访问')
#
#     @password.setter
#     def password(self, password):
#         """ 密码属性可写不可读
#         :param password: 用户密码
#         """
#         self.password_hash = generate_password_hash(password)
#
#     def verify_password(self, password):
#         """ 密码验证
#         :param password: 用户密码
#         :return: 验证成功返回 True，反之返回 False
#         """
#         return check_password_hash(self.password_hash, password)
#
#     def generate_confirmation_token(self, expiration=3600):
#         """ 生成用于确认身份的密令
#         :param expiration: 密令有效时间，单位秒
#         :return: 验证密令
#         """
#         s = Serializer(current_app.config['SECRET_KEY'], expiration)
#         return s.dumps({'confirm': self.id})
#
#     def confirm(self, token):
#         """ 利用密令确认账户
#         :param token: 验证密令
#         :return:
#         """
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)   # 解密密令
#         except:
#             return False
#         if data.get('confirm') != self.id:
#             return False
#         self.confirmed = True       # 一旦成功确认 confirmed 属性设置为 True
#         db.session.add(self)
#         return True
#
#     def generate_auth_token(self, expiration):
#         s = Serializer(current_app.config['SECRET_KEY'],
#                        expires_in=expiration)
#         return s.dumps({'id': self.id})
#
#     @staticmethod
#     def verify_auth_token(token):
#         s = Serializer(current_app.config['SECRET_KEY'])
#         try:
#             data = s.loads(token)
#         except:
#             return None
#         return User.query.get(data['id'])
#
#     def can(self, permissions):
#         """ 权限判断
#         利用逻辑运算符 &，如果经过 & 运算后仍为原先权限常量值，即确定用于拥有该权限。
#         :param permissions: 指定权限
#         :return: 验证成功返回 True，反之返回 False
#         """
#         return self.role is not None and \
#                (self.role.permissions & permissions) == permissions
#
#     @property
#     def is_administrator(self):
#         """ 判断是否为管理员
#         :return: 是管理员返回 True，反之返回 False
#         """
#         return self.can(Permission.ADMINISTER)
#
#     def update_last_seen(self):
#         """ 更新用于最近一次登录时间
#         """
#         self.last_seen = datetime.utcnow()
#         db.session.add(self)
#
#     def gravatar(self, size=100, default='identicon', rating='g'):
#         """ 利用哈希值生成头像
#         :param size: 头像大小
#         :param default:
#         :param rating:
#         :return: 头像链接
#         """
#         if request.is_secure:       # https 类型
#             url = 'https://secure.gravatar.com/avatar'
#         else:                       # http 类型
#             url = 'http://www.gravatar.com/avatar'
#         _hash = self.avatar_hash or hashlib.md5(
#             self.email.encode('utf-8')).hexdigest()
#         return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
#             url=url, hash=_hash, size=size, default=default, rating=rating)
#
#     @staticmethod
#     def generate_fake_users(count=100):
#         from sqlalchemy.exc import  IntegrityError
#             try:
#                 db.session.commit()
#             except IntegrityError:
#                 db.session.rollback()
#
#     def to_json(self, posts):
#         return {
#             'username': self.username,
#             'memberSince': self.member_since,
#             'lastSeen': self.last_seen,
#             'postCount': self.posts.count(),
#             'posts': posts
#         }
#     def __repr__(self):
#         return '<User {}>'.format(self.username)


# class AnonymousUser(AnonymousUserMixin):
#     """匿名用户（游客）模型"""
#     def can(self, permissions):
#         """ 游客没有任何权限
#         :param permissions: 指定权限
#         :return: 无任何权限
#         """
#         return False
#
#     @property
#     def is_administrator(self):
#         """ 判断是或否为管理员
#         :return: 非管理员
#         """
#         return False
#
# login_manager.anonymous_user = AnonymousUser    # 将未登录用户赋予游客模型


# @login_manager.user_loader
# def load_user(user_id):
#     """ Flask-Login 回调函数，用于指定标识符加载用户
#     :param user_id: 用户 id
#     :return: 查询到的用户对象
#     """
#     return User.query.get(int(user_id))

# class Post(db.Model):
#     """微博模型"""
#     __tablename__ = 'bbs_posts'     # 数据库表名
#     id = db.Column(db.Integer, primary_key=True)                                # 微博 id
#     body = db.Column(db.Text)                                                   # 微博内容
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # 发布时间
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))                # 作者 id
#     comments = db.relationship('Comment', backref='post', lazy='dynamic')       # 评论
#
#     @staticmethod
#     def generate_fake_posts(count=100):
#         from random import seed, randint
#         import forgery_py
#
#         seed()
#         user_count = User.query.count()
#         for i in range(count):
#             u = User.query.offset(randint(0, user_count - 1)).first()
#             p = Post(
#                 body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
#                 timestamp=forgery_py.date.date(True),
#                 author=u
#             )
#             db.session.add(p)
#             db.session.commit()
#
#     def to_json(self):
#         return {
#             'posTime': self.timestamp,
#             'post': self.body,
#             'authorID': self.author_id
#         }

# class Comment(db.Model):
#     """评论模型"""
#     __tablename__ = 'comments'      # 数据库表名
#     id = db.Column(db.Integer, primary_key=True)                                # 评论 id
#     body = db.Column(db.Text)                                                   # 评论内容
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # 评论时间
#     disabled = db.Column(db.Boolean)                                            # 是否被屏蔽
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'))                # 作者 id
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))                  # 微博 id
#
#     def to_json(self):
#         return {
#             'postTime': self.timestamp,
#             'post': self.body,
#             'postID': self.post_id,
#             'authorID': self.author_id
#         }

