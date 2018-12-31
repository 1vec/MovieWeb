from flask import g, current_app
from flask.cli import with_appcontext
import sqlite3
import click


def get_db(): #获取sqlite对象
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None): #关闭数据库
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(): #初始化数据库
    db = get_db()
    with current_app.open_resource('schema.sql') as fin:
        db.executescript(fin.read().decode('utf-8'))


@click.command('init-db') #用命令行初始化数据库
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app): #初始化app有关数据库的设置
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

