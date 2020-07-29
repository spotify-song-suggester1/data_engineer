import sqlite3
import pandas as pd 
from pandas import DataFrame

conn = sqlite3.connect('spotitry_songs.db')
curs = conn.cursor()

SQL_Query = pd.read_sql_query(
'''
SELECT *
from spotitry_songs
''',
conn)

df = pd.DataFrame(SQL_Query, columns=['id','name','energy',
                                      'liveness','danceability','instrumentalness','loudness',
                                      'speechiness','valence','tempo',])

print(df.head())
