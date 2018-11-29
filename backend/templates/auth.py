from flask import Blueprint, request, render_template
from backend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        #TODO
    return render_template('auth/login.html')
