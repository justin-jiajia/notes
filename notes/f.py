from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, BooleanField, HiddenField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from notes.m import Users


class LoginForm(FlaskForm):
    UserName = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    Password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    Remember = BooleanField('记住我')
    Submit = SubmitField('登录')


class SignUpForm(FlaskForm):
    UserName = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    Password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    Password2 = PasswordField('请再次输入密码', validators=[EqualTo('Password', message='两次输入的内容不一致')])
    Submit = SubmitField('注册')

    def validate_UserName(form, field):
        if Users.query.filter_by(name=field.data):
            raise ValidationError('用户名已存在')


class New(FlaskForm):
    Tittle = StringField('标题', validators=[DataRequired(message='请输入标题')])
    Body = CKEditorField('内容', validators=[DataRequired(message='请输入内容')])
    Submit = SubmitField('保存')


class Edit(FlaskForm):
    Tittle = StringField('标题', validators=[DataRequired(message='请输入标题')])
    Body = CKEditorField('内容', validators=[DataRequired(message='请输入内容')])
    Submit = SubmitField('修改')


class Del(FlaskForm):
    N_id = HiddenField('ID')
    Submit = SubmitField('删除')
