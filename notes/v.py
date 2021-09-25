from uuid import uuid4
from os.path import join as path_join
from flask_ckeditor import upload_fail, upload_success
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_required, login_user, logout_user
from flask import Blueprint, abort, flash, redirect, render_template, request, send_from_directory, url_for, current_app

from notes.e import db
from notes.h import to_safe, clean
from notes.m import Notes, Users
from notes.f import Del, Edit, LoginForm, New, SignUpForm

main = Blueprint('main', __name__)


@main.route('/login/', methods=['GET', 'POST'])
def get_login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    else:
        if form.validate_on_submit():
            u = Users.query.filter_by(name=form.UserName.data).one_or_none()
            if u and check_password_hash(u.password, form.Password.data):
                login_user(u, remember=form.Remember.data)
                flash('登陆成功！欢迎回来')
                return redirect(url_for('main.index'))
            else:
                flash('密码或用户名错误', 'error-alert')
                return redirect(url_for('main.get_login'))
        else:
            return render_template('login.html', form=form)


@main.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/sign-up/', methods=['GET', 'POST'])
def sign_up():
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        a_user = Users(name=sign_up_form.UserName.data, password=generate_password_hash(sign_up_form.Password.data))
        db.session.add(a_user)
        db.session.commit()
        login_user(a_user)
        flash('注册成功！')
        return redirect(url_for('main.index'))
    else:
        return render_template('sign_up.html', form=sign_up_form)


@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index_not_login.html')
    del_form = Del()
    notes = Notes.query.order_by(Notes.time_stamp.desc()).with_parent(current_user). \
        paginate(request.args.get('page', 1, type=int), per_page=5)
    return render_template('index.html', page=notes, del_note=del_form)


@main.route('/new/', methods=['GET', 'POST'])
@login_required
def new():
    form = New()
    if form.validate_on_submit():
        note = Notes(tittle=to_safe(form.Tittle.data), body=to_safe(form.Body.data), clean_body=clean(form.Body.data),
                     u_id=current_user.id, uuid=uuid4().hex)
        db.session.add(note)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('main.index'))
    else:
        return render_template('new.html', form=form)


@main.route('/edit/<int:p_id>/', methods=['GET', 'POST'])
@login_required
def edit_note(p_id):
    form = Edit()
    note = Notes.query.get_or_404(p_id)
    if note.u_id != current_user.id:
        abort(403)
    if form.validate_on_submit():
        if note.tittle == form.Tittle.data and note.body == form.Body.data:
            flash('笔记未修改，无需保存')
            return redirect(url_for('main.index'))
        note.tittle = to_safe(form.Tittle.data)
        note.body = to_safe(form.Body.data)
        note.clean_body = clean(form.Body.data)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('main.index'))
    else:
        form.Tittle.data = note.tittle
        form.Body.data = note.body
        return render_template('edit.html', form=form)


@main.route('/del/', methods=['POST'])
@login_required
def del_note():
    form = Del()
    if form.validate_on_submit():
        note = Notes.query.get_or_404(form.N_id.data)
        if note.u_id != current_user.id:
            abort(403)
        db.session.delete(note)
        db.session.commit()
        flash('删除成功！')
        return redirect(url_for('main.index'))
    else:
        abort(403)


@main.route('/v/<int:p_id>/')
@login_required
def v(p_id):
    note = Notes.query.get_or_404(p_id)
    del_form = Del()
    if note.u_id != current_user.id:
        abort(403)
    return render_template('v.html', note=note, del_note=del_form)


@main.route('/share/<string:uuid>/')
def share(uuid):
    note = Notes.query.filter_by(uuid=uuid).one_or_none()
    if note is None:
        abort(404)
    else:
        return render_template('share.html', note=note)


@main.route('/search/')
def search():
    q = request.args.get('q', '')
    if q == '':
        flash('请输入搜索内容！')
        return redirect(url_for('main.index'))
    del_form = Del()
    notes = Notes.query.whooshee_search(q).order_by(Notes.time_stamp.desc()).with_parent(current_user). \
        paginate(request.args.get('page', 1, type=int), per_page=5)
    return render_template('search.html', page=notes, del_note=del_form, q=q)


@main.route('/files/<path:filename>/')
def uploaded_files(filename):
    return send_from_directory(path_join(current_app.root_path, 'upload'), filename)


@main.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')  # 获取上传图片文件对象
    # Add more validations here
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:  # 验证文件类型示例
        return upload_fail(message='请上传图片!')  # 返回upload_fail调用
    filename = uuid4().hex + '.' + extension
    f.save(path_join(current_app.root_path, 'upload', filename))
    url = url_for('main.uploaded_files', filename=filename)
    return upload_success(url=url)  # 返回upload_success调用
