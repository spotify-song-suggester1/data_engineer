""" Prediction of preferred songs based on song input"""
from sprs.spotify import get_features, we_recommend, add_song, track_id_for_artist_title
from sqlalchemy import create_engine
import pandas as pd
from pandas import DataFrame
import sqlite3
from sklearn.neighbors import NearestNeighbors
import json
def predict_best_songs(track_id):
    """Determines and returns which user is more likely to say a given Tweet"""
    #This will give us a list of features necessary for prediction
    #Code by Ekaterina & Hernan
    song_to_predict = get_features(track_id)
    #Add song to existing DB
    #Code by Hernan
    add_song(song_to_predict)
    #This K Means model will give us a list of recommended songs
    #Code by Josh
    def predicto(track_id):
        # Instantiate and fit knn to the correct columns
        knn = NearestNeighbors(n_neighbors=20)
        knn.fit(df[df.columns[5:]])
        obs = df.index[df['id'] == track_id]
        series = df.iloc[obs, 5:].to_numpy()
        neighbors = knn.kneighbors(series)
        new_obs = neighbors[1][0][6:20]
        return list(df.loc[new_obs, 'id'])
    #Converting the DB to a DF to run a K Means model through
    conn = sqlite3.connect('sprs/spotitry_songs.db')
    curs = conn.cursor()
    SQL_Query = pd.read_sql_query(''' SELECT * from song ''',conn)
    df = pd.DataFrame(SQL_Query, columns=['id','name','energy',
                                      'liveness','danceability','instrumentalness','loudness',
                                      'speechiness','valence','tempo'])
    track_list = predicto(track_id)
    #Here we'll turn our list of track ids into song names
    #Code by Ekaterina & Hernan
    #Re-written by Hernan to return json with feature list
    suggestions = get_features(track_list[0])
    column_names = ['track_id', 'name', 'acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                    'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    final = pd.DataFrame([suggestions], columns=column_names)
    result = final.to_json()
    return result