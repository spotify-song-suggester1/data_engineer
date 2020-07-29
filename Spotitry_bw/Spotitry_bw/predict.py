""" Prediction of preferred songs based on song input"""
from .spotify import get_features, we_recommend, add_song, track_id_for_artist_title
from .keys import client_id, client_secret
from sqlalchemy import create_engine
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def predict_best_songs(song_name, artist_name):
    """Determines and returns which user is more likely to say a given Tweet"""

    #Store track id to variable
    track_id = track_id_for_artist_title(artist_name, song_name)

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
    engine = create_engine('sqlite:///db.sqlite3')
    sql = 'SELECT * FROM song'

    df = pd.read_sql(sql=sql, con=engine)
    
    track_list = predicto(track_id)
    
    #Here we'll turn our list of track ids into song names
    #Code by Ekaterina & Hernan
    suggestions = we_recommend(track_list)

    return suggestions