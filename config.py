import os
import datetime

# debug
DEBUG = True

# secret_key
SECRET_KEY = os.urandom(24)

# DataBase
HOST = "127.0.0.1"
PORT = "3306"
USERNAME = "root"
PASSWORD = "123456"
DB = "flask_bbs"

DB_URI = "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}?charset=utf8".format(
    user=USERNAME,
    pwd=PASSWORD,
    host=HOST,
    port=PORT,
    db=DB
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True

# permanent
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)

# session key
CMS_USER_ID = "Admin"

# # email config
# # 发送者邮箱的服务器地址
# MAIL_SERVER = "smtp.qq.com"
# MAIL_PORT = 465  # 非加密协议端口号为25
# MAIL_USE_TLS = False    # 端口号587
# MAIL_USE_SSL = True    # 端口号465
# MAIL_USERNAME = "954013871@qq.com"
# MAIL_PASSWORD = "pwwibvirfgrzbfae"
# MAIL_DEFAULT_SENDER = "954013871@qq.com"

# MAIL_SERVER: "smtp.163.com"
# MAIL_PORT: 25
# MAIL_USE_TLS: True
# MAIL_USERNAME: "beok02089163@163.com"
# MAIL_PASSWORD: "MWXVMWVPOLVKDRMB"
# MAIL_DEFAULT_SENDER: "beok02089163@163.com"
