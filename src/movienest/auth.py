from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from movienest.db import get_db
import functools
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')
re_password = re.compile(r'\w{8,16}$', flags=re.ASCII)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username, )
        ).fetchone()
        error = None

        if user is None:
            error = '请输入用户名'
        elif password is None:
            error = '请输入密码'
        elif not check_password_hash(user['password'], password):
            error = '密码错误'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('movienest.home'))
        flash(error)
    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if username is None:
            error = '请输入用户名'
        elif password is None:
            error = '请输入密码'
        elif db.execute(
                'SELECT id FROM user where username = ?',
                (username, )
        ).fetchone() is not None:
            error = '用户已存在'
        elif check_valid_password(password) is False:
            error = '密码应为8-16位字母、数字'

        if error is None:
            db.execute(
                'INSERT INTO USER (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/password', methods=('GET', 'POST'))
@login_required
def password():
    if request.method == 'POST':
        password = request.form['password1']
        password2 = request.form['password2']
        db = get_db()
        error = None

        if password is None:
            error = '请输入密码'
        elif password != password2:
            error = '两次输入密码不一致'
        elif check_valid_password(password) is False:
            error = '密码应为8-16位字母、数字'
        if error is None:
            db.execute(
                'UPDATE user '
                'SET password = ? '
                'WHERE id = ?',
                (generate_password_hash(password), g.user['id'])
            )
            db.commit()
            return redirect(url_for('movienest.home'))
        flash(error)
    return render_template('auth/password.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('movienest.home'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?',
            (user_id, )
        ).fetchone()

def check_valid_password(pwd):
    if re_password.match(pwd) is None:
        return False
    return True
