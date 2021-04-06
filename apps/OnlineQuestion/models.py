# -*- coding: utf-8 -*-
# @Time    : 2020/12/12 12:13
# @Author  : JAKE4545
# @Email   : tmwu2018@163.com
from exts import db
from datetime import datetime

class MarxQuestionBank(db.model):
    __tablename__ = "Marx"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.String(300))
    answer = db.Column(db.String(200))
    options = db.Column(db.String(300))

