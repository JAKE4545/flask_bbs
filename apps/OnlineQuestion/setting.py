# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 10:44
# @Author  : JAKE4545
# @Email   : tmwu2018@163.com
import os
# __file__ refers to the file settings.py
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'source')