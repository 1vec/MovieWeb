from flask import Blueprint, render_template
from backend.auth import login_required

bp = Blueprint('analysis', __name__)


@bp.route('/home')
def home():
    return render_template('home.html')


@bp.route('/box-office')
@login_required
def box_office():
    return render_template('box-office.html')


@bp.route('/rating')
@login_required
def rating():
    return render_template('rating.html')
