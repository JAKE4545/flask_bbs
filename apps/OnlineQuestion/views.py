# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 14:39
# @Author  : JAKE4545
# @Email   : tmwu2018@163.com
from flask import (
    Blueprint, render_template
)
from apps.decorators import login_required

OnlineQuestion = Blueprint("OnlineQuestion", __name__, url_prefix="/OnlineQuestion")

@OnlineQuestion.route("/", endpoint="home")
@login_required
def home():
    return render_template("")
