import sqlite3

test_data = [
        ('红海行动', ('潘施敏', '李婉婷'), 666666, '2018-12-18', 9.9, '潘施敏', ('动作', '悬疑', '爱情')),
        ('红海hhh', ('李婉婷', '许泷方'), 77777, '2018-12-13', 6.8, '潘施敏', ('动作', '恐怖'))]

def get_id_by_name(db, table_name, name):
    command = 'SELECT id FROM {} WHERE name = ?'.format(table_name)
    print(command)
    return db.execute(
            command,
            (name, )).fetchone()['id']

def init_record(db, table_name, name):
    command = 'INSERT INTO {0:} (name) SELECT ? WHERE NOT EXISTS(SELECT 1 FROM {0:} WHERE name = ?)'.format(table_name)
    print(command)
    return db.execute(
            command,
            (name, name))

if __name__ == '__main__':
    db = sqlite3.connect(
            'db.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
            )
    db.row_factory = sqlite3.Row

    for name, actors, box_office, date, score, director, types in test_data:
        db.execute(
                'INSERT INTO movies (name, director, box_office, date, score)'
                'VALUES (?, ?, ?, ?, ?)', (name, director, box_office, date, score)
                )
        movie_id = get_id_by_name(db, 'movies', name)
        for actor in actors:
            init_record(db, 'actors', actor)
            actor_id = get_id_by_name(db, 'actors', actor)
            db.execute(
                    'INSERT INTO movie_actor (movie_id, actor_id) VALUES'
                    '(?, ?)', (movie_id, actor_id))
        for tp in types:
            init_record(db, 'types', tp)
            type_id = get_id_by_name(db, 'types', tp)
            db.execute(
                    'INSERT INTO movie_type (movie_id, type_id) VALUES'
                    '(?, ?)', (movie_id, type_id))
        db.commit()
