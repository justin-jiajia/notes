from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_whooshee import Whooshee

db = SQLAlchemy()
moment = Moment()
login = LoginManager()
cke = CKEditor()
whoshee = Whooshee()


@login.user_loader
def load_user(user_id):
    from notes.m import Users
    user = Users.query.get(int(user_id))
    return user


login.login_view = 'main.get_login'
login.login_message = '请先登录！'
