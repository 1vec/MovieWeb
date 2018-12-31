import sqlite3

if __name__ == '__main__':
    db = sqlite3.connect('db.sqlite')
    with open('scrapy.sql') as f:
        db.executescript(f.read())
