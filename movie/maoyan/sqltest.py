import sqlite3
import pandas as pd

with sqlite3.connect('scrapy.db') as con:
    df = pd.read_sql(sql='SELECT name FROM movies', con=con)

print(df['name'].tolist())