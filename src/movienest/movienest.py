from flask import Blueprint, render_template
from movienest.auth import login_required
from movienest.db import get_db

bp = Blueprint('movienest', __name__)


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

@bp.route('/resource', methods=['POST'])
def hello():
    req = request.get_json()
    code = int(req['type'])
    if code == 0:
        data = count_type(req['startm'], req['endm'])
    elif code == 1:
        data = count_type_monthly(req['startm'], req['endm'])
    elif code == 2:
        data = box_type(req['startm'], req['endm'])
    elif code == 3:
        data = box_type_monthly(req['startm'], req['endm'])
    elif code == 4:
        data = rate_range(req['startm'], req['endm'])
    return Response(json.dumps(data))

def count_type(start, end):
    result = {}
    db = get_db()
    print(start, end)
    for each_movie in db.execute(
            'SELECT type FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ?',
            (start, end)).fetchall():
        for each_type in json.loads(each_movie['type']):
            result.setdefault(each_type, 0)
            result[each_type] += 1
    try:
        result.pop('None')
    except:
        pass

    for each in tuple(result.keys()):
        if result[each] <= 3:
            result.pop(each)
    return result

def count_type_monthly(start, end):
    result = {}
    unique_date = set()
    db = get_db()
    print(start, end)
    for each_movie in db.execute(
            'SELECT type, substr(date, 1, 7) FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ?',
            (start, end)).fetchall():
        for each_type in json.loads(each_movie['type']):
            date = each_movie['substr(date, 1, 7)']
            unique_date.add(date)
            result.setdefault(each_type, {})
            result[each_type].setdefault(date, 0)
            result[each_type][date] += 1
    try:
        result.pop('None')
    except:
        pass
    
    unique_date = list(unique_date)
    unique_date.sort()
    for tp, count in result.items():
        result[tp] = []
        for date in unique_date:
            result[tp].append(count.get(date, 0))

    top_five = sorted(result.items(), key = lambda d: sum(d[1]), reverse=True)
    top_five = dict(top_five[:5])

    return (unique_date, top_five)

def box_type(start, end):
    result = {}
    db = get_db()
    print(start, end)
    for each_movie in db.execute(
            'SELECT type, box_office FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ?',
            (start, end)).fetchall():
        for each_type in json.loads(each_movie['type']):
            result.setdefault(each_type, 0)
            if each_movie['box_office'] is not None:
                result[each_type] += each_movie['box_office']
    try:
        result.pop('None')
    except:
        pass

    for each in tuple(result.keys()):
        if result[each] <= 3:
            result.pop(each)
    return result

def box_type_monthly(start, end):
    result = {}
    unique_date = set()
    db = get_db()
    print(start, end)
    for each_movie in db.execute(
            'SELECT type, substr(date, 1, 7), box_office FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ?',
            (start, end)).fetchall():
        for each_type in json.loads(each_movie['type']):
            date = each_movie['substr(date, 1, 7)']
            unique_date.add(date)
            result.setdefault(each_type, {})
            result[each_type].setdefault(date, 0)
            if each_movie['box_office'] is not None:
                result[each_type][date] += each_movie['box_office']
    try:
        result.pop('None')
    except:
        pass
    
    unique_date = list(unique_date)
    unique_date.sort()
    for tp, count in result.items():
        result[tp] = []
        for date in unique_date:
            result[tp].append(count.get(date, 0))

    top_five = sorted(result.items(), key = lambda d: sum(d[1]), reverse=True)
    top_five = dict(top_five[:5])

    return (unique_date, top_five)

def rate_range(start, end):
    db = get_db()
    result = []
    sorted_movies = db.execute(
            'SELECT name, score FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ?'
            'ORDER BY score desc', (start, end)).fetchall()
    for i in range(10):
        each_movie = sorted_movies[i]
        result.append([each_movie['name'], each_movie['score']])
    return result
