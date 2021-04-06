from flask import (
    Blueprint, render_template, views, session,
    request, redirect, url_for, g, flash
)
from .forms import LoginForm, SetPwdForm, VerifyEmailForm, RegisterForm,PostForm
from .models import CMSUser, Post, PwdRecord, MarxQuestionBank
from exts import db
from apps.decorators import login_required
from utils import restful
import config

cms = Blueprint("cms", __name__, url_prefix="/cms")

@cms.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        nickname = form.nickname.data
        email = form.email.data
        password = form.password.data
        user = CMSUser(username=nickname,
                       password=password,
                       email=email)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请登录')
        return redirect(url_for('cms.home'))
    else:
        flash('注册失败，请重试')
        return render_template("cms/register.html", form=form)

@cms.route("/", endpoint="home")
@login_required
def home():
    return render_template("cms/cms_base.html")

@cms.route("/logout/", endpoint="logout")
@login_required
def logout():
    del session[config.CMS_USER_ID]
    return redirect(url_for("cms.login"))

@cms.route("/index/", endpoint="index")
@login_required
def index():
    posts = Post.query.all()
    if request.method == "POST":
        pass
    return render_template("cms/index.html", post_msg=posts)

@cms.route("/my_posts/", endpoint="my_posts")
@login_required
def my_posts():
    my_posts = Post.query.filter_by(author_id=session[config.CMS_USER_ID]).all()
    if request.method == "POST":
        pass
    return render_template("cms/my_index.html", post_msg=my_posts)

# 查看资料
@cms.route("/profile/", endpoint="profile", methods=["GET", ])
@login_required
def profile():
    return render_template("cms/profile.html")

# 通过类的方式创建表单验证
class SetEmailView(views.MethodView):
    """修改邮箱"""
    decorators = [login_required]
    def get(self):
        return render_template("cms/setemail.html")

    def post(self):
        form = VerifyEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.param_error("验证失败")

class SetPwdView(views.MethodView):
    decorators = [login_required]
    """修改密码"""
    def get(self, error=None, message=None):
        return render_template("cms/setpwd.html", error=error, message=message)

    def post(self):
        form = SetPwdForm(request.form)
        if form.validate():
            raw_password = form.raw_password.data
            password = form.password.data
            error = None
            message = None
            if not g.cms_user.check_password(raw_password):
                error = "原密码错误"
            elif raw_password == password:
                error = "不能使用原密码作为新密码"
            else:
                g.cms_user.password = password
                db.session.commit()
                # 此处添加到history_pwd数据库中
                # history_pwd = PwdRecord(password=password,
                #                         user_id=session[config.CMS_USER_ID])
                # db.session.add(history_pwd)
                # db.session.commit()
                message = "修改成功"
            return self.get(error=error, message=message)
        else:
            return self.get(error=form.errors)

class LoginView(views.MethodView):
    def get(self, error=None):
        return render_template("cms/login.html", error=error)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for("cms.home"))
            else:
                return self.get(error="邮箱或密码错误")
        else:
            error = form.errors.get("password")[0]
            return self.get(error=error)

cms.add_url_rule("/login/", view_func=LoginView.as_view("login"))
cms.add_url_rule("/setpwd/", view_func=SetPwdView.as_view("setpwd"))
cms.add_url_rule("/setemail/", view_func=SetEmailView.as_view("setemail"))


@cms.route('/OnlineQuestion/', endpoint='OnlineQuestion')
@login_required
def hello():
    return render_template('OnlineQuestion/hello.html')

@cms.route('/post', endpoint='post', methods=['GET', 'POST'])
@login_required
def posts():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        _post = Post(body=form.text.data,
                     author_id=session[config.CMS_USER_ID])
        db.session.add(_post)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('cms.home'))
    else:
        return render_template('post.html')

# @cms.route('/OnlineQuestion/<int:id>')
# @login_required
# def practive(id):
#     pass

@cms.route("/OnlineQuestion/<int:id>", methods=['POST', 'GET'])
@login_required
def prative(id):
    data = MarxQuestionBank.query.all()
    item = data[id]
    html_data = {}
    html_data['qestion'] = str(id)+'、'+item.question
    options = item.options.split("&")
    for i in range(len(options)):
        html_data['option'+chr(ord('A')+i)] = options[i]
    html_data['last'] = str(id - 1)
    html_data['next'] = str(id + 1)
    html_data['answer'] = str(id) + '/answer'
    return render_template('OnlineQuestion/qestion.html', **html_data)

@cms.route('/OnlineQuestion/<int:id>/answer', methods=['GET','POST'])
@login_required
def answer(id):
    item = MarxQuestionBank.query.filter_by(id=id).first()
    flash('正确答案：'+item.answer)
    return redirect(url_for('cms.prative', id=id))