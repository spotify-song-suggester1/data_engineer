import sqlite3
import pandas as pd 
from pandas import DataFrame

conn = sqlite3.connect('spotitry_songs.db')
curs = conn.cursor()

curs.execute('''
CREATE TABLE spotitry_songs(
    id VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    energy REAL,
    liveness REAL,
    danceability REAL,
    instrumentalness REAL,
    loudness REAL,
    speechiness REAL,
    valence REAL,
    tempo REAL)
'''
)

conn.commit()


read_clients = pd.read_csv (r'/Users/josh/Documents/Lambda/Unit 4/data_engineer/Spotitry_bw/Spotitry_bw/spotitry_songs.csv')
read_clients.to_sql('spotitry_songs', conn, if_exists='append', index = False) 
