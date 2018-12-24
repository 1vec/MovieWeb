from flask import Blueprint, render_template, request, Response
from movienest.auth import login_required
from movienest.db import get_db
import json

bp = Blueprint('movienest', __name__)


@bp.route('/')
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


@bp.route('/search')
@login_required
def search():
    return render_template('search.html')

@bp.route('/listing')
@login_required
def listing():
    return render_template('listing.html')

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
        data = rank_score(req['startm'], req['endm'])
    elif code == 5:
        data = get_model(req['startm'], req['endm'])
    elif code == 6:
        data = box_yearly(req['startm'], req['endm'])
    elif code == 7:
        data = get_listing(req['startm'], req['endm'], req['mtype'])
    elif code == 8:
        data = search_db(req['stype'], req['keyword'])
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

    top_five = sorted(result.items(), key=lambda d: sum(d[1]), reverse=True)
    top_five = dict(top_five[:5])

    return unique_date, top_five


def box_type(start, end):
    result = []
    db = get_db()
    print(start, end)
    for each in db.execute(
            'SELECT t.name, sum(box_office) value '
            'FROM movie_type mt '
            'JOIN movies m ON m.id = mt.movie_id '
            'JOIN types t ON t.id = mt.type_id '
            'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
            'GROUP BY t.name '
            'ORDER BY value DESC '
            'LIMIT 25',
            (start, end)).fetchall():
        result.append(tuple(each))
    print(result)
    return result


def box_type_monthly(start, end):
    db = get_db()
    unique_date = db.execute(
        'SELECT DISTINCT substr(date, 1, 7)'
        'FROM movies '
        'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
        'ORDER BY date',
        (start, end)).fetchall()
    mtype = db.execute(
        'SELECT DISTINCT t.name '
        'FROM movie_type mt '
        'JOIN movies m ON m.id = mt.movie_id '
        'JOIN types t ON t.id = mt.type_id '
        'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
        'LIMIT 5',
        (start, end)).fetchall()
    unique_date = [x[0] for x in unique_date]
    result = {}
    for tp, *other in mtype:
        result.setdefault(tp, list())
        for month in unique_date:
            result[tp].append(db.execute(
                'SELECT sum(box_office) value '
                'FROM movie_type mt '
                'JOIN movies m ON m.id = mt.movie_id '
                'JOIN types t ON t.id = mt.type_id '
                'WHERE substr(date, 1, 7) = ? AND t.name = ? ',
                (month, tp)).fetchone()['value'])
    return unique_date, result

def box_yearly(start, end, mtype=None):
    db = get_db()
    unique_year = db.execute(
        'SELECT DISTINCT substr(date, 1, 4)'
        'FROM movies '
        'WHERE ? <= substr(date, 1, 4) AND substr(date, 1, 4) <= ? '
        'ORDER BY date',
        (start, end)).fetchall()
    unique_year = [x[0] for x in unique_year]
    result = {}
    for year in unique_year:
        result[year] = list()
        for i in range(1, 13):
            month = '{}-{:02d}'.format(year, i)
            print(month)
            if mtype is not None:
                result[year].append(db.execute(
                    'SELECT sum(box_office) value '
                    'FROM movie_type mt'
                    'JOIN movies m ON m.id = mt.movie_id '
                    'JOIN types t ON t.id = mt.type_id '
                    'WHERE substr(date, 1, 7) = ? AND t.name = ? ',
                    (month, mtype)).fetchone()['value'])
            else:
                result[year].append(db.execute(
                    'SELECT sum(box_office) value '
                    'FROM movies '
                    'WHERE substr(date, 1, 7) = ?',
                    (month, )).fetchone()['value'])
    print(result)
    return [i for i in range(1, 13)], result


def rank_score(start, end):
    db = get_db()
    result = []
    for each in db.execute(
            'SELECT name, score FROM movies WHERE'
            '? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
            'ORDER BY score DESC '
            'LIMIT 10',
            (start, end)).fetchall():
        result.append(tuple(each))
    print(result)
    return result


def get_model(start, end):
    db = get_db()
    result = []
    for each in db.execute(
            'SELECT a.name, count(*) times '
            'FROM movie_actor ma '
            'JOIN movies m ON m.id = ma.movie_id '
            'JOIN actors a ON a.id = ma.actor_id '
            'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
            'GROUP BY actor_id '
            'ORDER BY times DESC '
            'LIMIT 15',
            (start, end)).fetchall():
        result.append(tuple(each))
    return result

def get_listing(start, end, mtype=None):
    db = get_db()
    result = []
    if mtype is None:
        movies = db.execute(
                'SELECT id, name, date, score FROM movies '
                'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? '
                'ORDER BY score DESC '
                'LIMIT 50',
                (start, end)).fetchall()
    else:
        movies = db.execute(
                'SELECT m.id id, m.name name, date, score '
                'FROM movie_type mt '
                'JOIN movies m ON m.id = mt.movie_id '
                'JOIN types t ON t.id = mt.type_id '
                'WHERE ? <= substr(date, 1, 7) AND substr(date, 1, 7) <= ? AND t.name = ? '
                'ORDER BY score DESC '
                'LIMIT 50',
                (start, end, mtype)).fetchall()
    print(movies)
    for each in movies:
        actors = db.execute(
                'SELECT a.name '
                'FROM movie_actor ma '
                'JOIN actors a ON ma.actor_id = a.id '
                'WHERE movie_id = ?',
                (each['id'], )).fetchall()
        gen = (a[0] for a in actors)
        actors = ', '.join(gen)
        types = db.execute(
                'SELECT t.name '
                'FROM movie_type mt '
                'JOIN types t ON mt.type_id = t.id '
                'WHERE movie_id = ?',
                (each['id'], )).fetchall()
        gen = (a[0] for a in types)
        types = ', '.join(gen)
        result.append({
            'name': each['name'],
            'date': each['date'],
            'score': each['score'],
            'actors': actors,
            'types': types
            })
    return result

def search_db(stype, keyword):
    db = get_db()
    if stype == 'name':
        movies = db.execute(
                'SELECT id, name, date, score FROM movies '
                'WHERE name = ? ',
                (keyword, )).fetchall()
    elif stype == 'director':
        movies = db.execute(
                'SELECT id, name, date, score FROM movies '
                'WHERE director = ? ',
                (keyword, )).fetchall()
    elif stype == 'actor':
        movies = db.execute(
                'SELECT m.id id, m.name name, date, score '
                'FROM movie_actor ma '
                'JOIN movies m ON m.id = ma.movie_id '
                'JOIN actors a ON ma.actor_id = a.id '
                'WHERE a.name = ?',
                (keyword, )).fetchall()
    print(stype, keyword)
    print(movies)
    result = []
    for each in movies:
        actors = db.execute(
                'SELECT a.name '
                'FROM movie_actor ma '
                'JOIN actors a ON ma.actor_id = a.id '
                'WHERE movie_id = ?',
                (each['id'], )).fetchall()
        gen = (a[0] for a in actors)
        actors = ', '.join(gen)
        types = db.execute(
                'SELECT t.name '
                'FROM movie_type mt '
                'JOIN types t ON mt.type_id = t.id '
                'WHERE movie_id = ?',
                (each['id'], )).fetchall()
        gen = (a[0] for a in types)
        types = ', '.join(gen)
        result.append({
            'name': each['name'],
            'date': each['date'],
            'score': each['score'],
            'actors': actors,
            'types': types
            })
    print(result)
    return result

