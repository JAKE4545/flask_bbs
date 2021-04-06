from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,SelectField
from wtforms.validators import DataRequired, Length
from ..cms import CMSUser


class PostForm(FlaskForm):
    """微博发布表单"""
    body = TextAreaField('此刻的感想？', validators=[DataRequired()])
    submit = SubmitField('发布')


class CommentForm(FlaskForm):
    """评论表单"""
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField('确认')


class EditProfileForm(FlaskForm):
    """用户编辑个人信息表单"""
    username = StringField('用户名',
                           validators=[DataRequired(), Length(1, 16)])
    realname = StringField('真实姓名', validators=[Length(0, 16)])
    sex = SelectField('性别', choices=[('男', '男'), ('女', '女')], coerce=str)
    location = StringField('地区', validators=[Length(0, 64)])
    about_me = TextAreaField('个人简介')
    submit = SubmitField('提交')


class SearchUserForm(FlaskForm):
    """搜索用户表单"""
    username = StringField('用户名', validators=[Length(0, 16)])
    submit = SubmitField('搜索')

    # def validate_username(self, filed):
    #     """ 验证用户名是否已被使用。魔法方法
    #     :param filed: 用户名数据
    #     """
    #     if filed.data != self.user.username and \
    #             CMSUser.query.filter_by(username=filed.data).first():
    #         raise ValidationError('该用户名已被使用')