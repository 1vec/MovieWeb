import sqlite3


db_name = 'scrapy0.db'

db_conn = sqlite3.connect(db_name)
db_cur = db_conn.cursor()

order = 'DELETE FROM movies WHERE "2015" < substr(date, 1, 4) AND substr(date, 1, 4) < "2017"'
db_cur.execute(order)
db_conn.commit()
db_conn.close()