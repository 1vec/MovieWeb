from flask import Blueprint, render_template, request, session, redirect, url_for, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
from movienest.db import get_db
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')


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
            error = 'Username is required.'
        elif password is None:
            error = 'Password is required.'
        elif not check_password_hash(user['password'], password):
            error = 'Password is invalid.'

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
            error = 'Username is required.'
        elif password is None:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user where username = ?',
                (username, )
        ).fetchone() is not None:
            error = 'User is already exists.'

        if error is None:
            db.execute(
                'INSERT INTO USER (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')


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


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
