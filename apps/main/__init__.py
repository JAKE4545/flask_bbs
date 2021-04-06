# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 21:14
# @Author  : JAKE4545
# @Email   : tmwu2018@163.com
from flask import Blueprint
from flask_login import current_user
main = Blueprint('main', __name__)


@main.app_context_processor
def inject_global_variable():
    """ 注入全局变量，在 jinja2 模板中可用"""
    return dict(current_user=current_user)

from . import views, errors     # 避免循环导入模块
