from flask_wtf import FlaskForm
from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import EqualTo, Length
from utils import cache
from wtforms import ValidationError

class RegisterForm(Form):
    nickname = StringField()
    email = StringField()
    password = StringField(validators=[Length(4, 20, message="密码格式不正确，长度在4-20之间！")])
    re_password = StringField(validators=[EqualTo("password", message="密码输入不一致")])


class LoginForm(Form):
    email = StringField()
    password = StringField(validators=[Length(4, 20, message="密码格式不正确，长度在4-20之间！")])
    remember = IntegerField()


class SetPwdForm(Form):
    raw_password = StringField()
    password = StringField(validators=[Length(4, 20, message="密码格式不正确，长度在4-20之间！")])
    repeat = StringField(validators=[EqualTo("password", message="密码输入不一致")])


class VerifyEmailForm(Form):
    # email = StringField(validators=[Email()])
    captcha = StringField(validators=[Length(6, 6, message="请输入正确长度的验证码")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = cache.get(email)
        if not captcha_cache or captcha_cache.lower() != captcha.lower():
            raise ValidationError("邮箱验证错误！")


class PostForm(Form):
    text = StringField(validators=[Length(1, 2000, message="发布的帖子太长或者太短，字数控制在1-2000之间！")])

