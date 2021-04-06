import json
from flask import render_template, flash, redirect, url_for, Blueprint
import os
from .setting import APP_STATIC
from apps.decorators import login_required

OnlineQuestion = Blueprint('OnlineQuestion', __name__, url_prefix="/OnlineQuestion")

with open(os.path.join(APP_STATIC, 'sum.json')) as f:
    data = json.load(f)

@OnlineQuestion.route("<int:id>")
@login_required
def prative(id):
    item = data[id]
    html_data = {}
    html_data['qestion'] = str(id)+'、'+item['question']
    for i, opt in enumerate(item['options']):
        html_data['option'+chr(ord('A')+i)] = opt
    html_data['last'] = str(id - 1)
    html_data['next'] = str(id + 1)
    html_data['answer'] = str(id) + '/answer'
    print(html_data)
    return render_template('OnlineQuestion/qestion.html', **html_data)

@OnlineQuestion.route('<int:id>/answer')
@login_required
def answer(id):
    item = data[id]
    flash('正确答案：'+item['answer'])
    return redirect(url_for('prative', id=id))