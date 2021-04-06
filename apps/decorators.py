import config
from flask import session, redirect, url_for
from functools import wraps
# from flask import abort
# from flask_login import current_user
# from .models import Permission

# def permission_required(permission):
#     """ 权限验证装饰器
#     :param permission: 指定权限
#     :return: 装饰器
#     """
#     def decorator(f):
#         @wraps(f)
#         def inner(*args, **kwargs):
#             if not current_user.can(permission):
#                 abort(403)
#             return f(*args, **kwargs)
#         return inner
#     return decorator
#
# def admin_required(f):
#     """ 管理员权限验证
#     :param f: 视图方法
#     :return: 装饰器
#     """
#     return permission_required(Permission.ADMINISTER)(f)

# 登录验证装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("cms.login"))
    return wrapper