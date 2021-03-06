from flask import Flask, render_template
from click import echo, option
from os import getenv


def create_app():
    # 配置主程序
    app = Flask("notes")
    app.secret_key = getenv('SECRET_KEY')
    app.config.update(
        SQLALCHEMY_DATABASE_URI=getenv('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        CKEDITOR_FILE_UPLOADER='/upload',
        CKEDITOR_ENABLE_CODESNIPPET=True,
        WHOOSHEE_MIN_STRING_LEN=1,
    )
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    # 注册蓝本
    from notes.v import main
    app.register_blueprint(main)

    # 注册扩展
    from notes.e import db, moment, login, cke, whoshee
    db.init_app(app)
    moment.init_app(app)
    login.init_app(app)
    cke.init_app(app)
    whoshee.init_app(app)
    # 注册自定义函数
    @app.cli.command()
    @option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            echo('Dropping...')
            db.drop_all()
            echo('Drop!')
        echo('Creating..')
        db.create_all()
        echo('OK!')

    @app.cli.command()
    def reindex():
        echo('Reindexing...')
        whoshee.reindex()
        echo('OK!')
    # 注册错误视图函数
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def page_not_found(e):
        return render_template("errors/403.html"), 403

    return app
