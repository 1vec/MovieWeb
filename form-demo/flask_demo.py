from flask import Flask, Response, render_template, request
import json
import sqlite3


app = Flask(__name__)

@app.route('/')
def res():
    return render_template('form.html')

@app.route('/resource', methods=['POST'])
def hello():
    print(request.get_json())
    data = count_type()
    return Response(json.dumps(data))

def count_type():
    result = {}
    db = sqlite3.connect(
        'scrapy.db',
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    for each_movie in db.execute('SELECT type FROM movies').fetchall():
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

if __name__ == '__main__':
    app.run()
