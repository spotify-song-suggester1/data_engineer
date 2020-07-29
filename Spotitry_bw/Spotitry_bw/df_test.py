import sqlite3
import pandas as pd 
from pandas import DataFrame
from sklearn.neighbors import NearestNeighbors

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

def predicto(track_id):

        # Instantiate and fit knn to the correct columns
        knn = NearestNeighbors(n_neighbors=20)
        knn.fit(df[df.columns[5:]])

        obs = df.index[df['id'] == track_id]
        series = df.iloc[obs, 5:].to_numpy()

        neighbors = knn.kneighbors(series)
        new_obs = neighbors[1][0][6:20]
        return list(df.loc[new_obs, 'id'])

track = '1SFIGzSh0dMRL7SH7nJJhX'

suggest = predicto(track)

print(suggest)
