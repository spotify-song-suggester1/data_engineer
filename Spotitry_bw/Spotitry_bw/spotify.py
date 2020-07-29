"""Retrieve songs and persist in database """
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .models import DB, Song
from .keys import client_id, client_secret
from os import getenv
from .token_api import SpotifyAPI

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

def get_features(track_id):
    """Gets track ID for song based on song and artist name"""

    meta_data = sp.track(track_id)
    features = sp.audio_features(track_id)

    name = meta_data['name']
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    duration_ms = meta_data['duration_ms']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    valence = features[0]['valence']

    track = [track_id, name, acousticness, danceability, duration_ms, energy, instrumentalness,
             liveness, loudness, speechiness, tempo, valence]
    
    return track



def we_recommend(track_list):

    for t in track_list:
        final_list = []
        final_list.append((sp.track(t))['name'])

    return final_list
   
    
    

def add_song(song_to_predict):
    """Add song to DB, if song exists do nothing"""

    try:
        song_id = song_to_predict[0]
        name = song_to_predict[1]
        energy = song_to_predict[5]
        liveness = song_to_predict[7]
        danceability = song_to_predict[3]
        instrumentalness = song_to_predict[6]
        loudness = song_to_predict[8]
        speechiness = song_to_predict[9]
        valence = song_to_predict[11]
        tempo = song_to_predict[10]

        add_stip = (Song.query.get(song_id) or
                    Song(id=song_id, name=name, energy=energy,
                         liveness=liveness, danceability=danceability,
                         instrumentalness=instrumentalness, loudness=loudness,
                         speechiness=speechiness, valence=valence, tempo=tempo))
        DB.session.add(add_stip)
    
    except Exception as e:
        print('Error processing {}: {}'.format(song_to_predict, e))
        raise e
    else:
        DB.session.commit()



# This will give us the track id of the song input by user (Code by Ekaterina)
def track_id_for_artist_title(artist, title):
    track_id = None
    spotif = SpotifyAPI(client_id, client_secret)
    res = spotif.search_artist_track(
        q_artist=artist, q_track=title)
    if (res['tracks']['items']) and (len(res["tracks"]["items"]) > 0):
        track_id = res["tracks"]["items"][0]["id"]
    return track_id

