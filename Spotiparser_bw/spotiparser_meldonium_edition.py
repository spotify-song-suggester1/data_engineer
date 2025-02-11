# -*- coding: utf-8 -*-
"""Copy of SpotifyBW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tAyzbtgvsCwo9zmz9uUmhcSUClg4-wcx
"""

from pandas.io.json import json_normalize
import pandas as pd
import json as json
import requests
import base64
import datetime
from urllib.parse import urlencode
import time
from os import getenv, path
import csv
import random
import time

# Readquitme: https://pypi.org/project/Random-Word/

client_id = getenv('CLIENT_ID')
client_secret = getenv('CLIENT_SECRET')
ALL_TRACKS = "all_tracks.csv"
ALL_ARTISTS = "all_artists.csv"
ALL_WORDS = "all_words.csv"

TRACK_IDS = []


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    # Need to add get_resources, so that we don't get rate-limited
    # (as in curl -X "GET" "https://api.spotify.com/v1/tracks?ids=7ouMYWpwJ422jRcDASZB7P%2C4VqPOruhp5EdPBeR92t6lQ%2C2takcwOaAZWiXQijPHIx7B&market=ES" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer ")

    # So I changed this method accordingly

    def get_resources(self, lookup_parameters, lookup_parameter_type="ids", resource_type='tracks', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}?{lookup_parameter_type}={lookup_parameters}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')

    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')

    def base_search(self, query_params):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, operator=None, operator_query=None, search_type='artist', limit=20, offset=0):
        if query == None:
            raise Exception("A query is required.")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        # adding limit and offset to the query
        query_params = urlencode(
            {"q": query, "type": search_type.lower(), "limit": limit, "offset": offset})
        print(query_params)
        return self.base_search(query_params)

# This class for wrangling received outputs


class TrackFeatureProcessor(object):
    track_js = None
    feat_js = None
    track_df = None
    feat_df = None
    df = None
    artists_df = None
    word = None
    word_df = None

    def __init__(self, track_js, feat_js, word, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.track_js = track_js
        self.feat_js = feat_js
        self.word = word

    def process_feats_track(self):
        self.process_features_json()
        self.process_track_json()
        # self.merge_track_features()

    def extract_artists_df(self):
        del(self.track_df["artists"])
        artists_cols = ["artist.id", "id", "artist.name"]
        self.artists_df = pd.json_normalize(
            self.track_js, "artists", meta="id", record_prefix="artist.")
        self.artists_df = self.clean_df(self.artists_df, artists_cols)

    def create_word_df(self):
        self.word_df = pd.DataFrame(
            {"word": self.word, "id": self.track_df["id"][0]}, index=[0])

    def process_features_json(self):
        our_features = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                        "instrumentalness", "liveness", "valence", "tempo", "id", "duration_ms", "time_signature"]
        self.feat_js = self.process_json(self.feat_js, our_features)
        self.feat_df = self.js_to_dataframe(self.feat_js)

    def process_track_json(self):
        our_features = ["album", "artists", "duration_ms",
                        "explicit", "id", "is_local", "name", "popularity"]
        album_features = ["album.name", "album.release_date"]
        cols_to_keep = our_features + album_features
        self.track_js = self.process_json(self.track_js, our_features)
        self.track_df = self.js_to_dataframe(self.track_js)
        self.track_df = self.clean_df(self.track_df, cols_to_keep)

    def merge_track_features(self):
        self.merged_df = pd.merge(
            self.track_df, self.feat_df, on='id', how='inner')

    def js_to_dataframe(self, processed_trjs):
        return pd.json_normalize(processed_trjs)

    def process_json(self, mjson, our_features):
        newj = {}
        for feat in our_features:
            newj[feat] = mjson[feat]
        return newj

    def clean_df(self, df_to_clean, cols_to_keep):
        return df_to_clean.loc[:, df_to_clean.columns.intersection(
            cols_to_keep)]

# Here we go - some demonstration

# lets search:


def get_records(file_name, column_name):
    # populate list of track ids
    result = []
    if path.exists(file_name):
        with open(file_name, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for lines in csv_reader:
                result.append(lines[column_name])
    return list(set(result))


def populate_processors(spotify, word, processors, collected_ids):
    af_resps = {}
    tr_resps = {}
    if len(collected_ids) > 0:
        # get tracks and audio features at once with the multiple resource method
        af_resps = spotify.get_resources(
            ','.join(map(str, collected_ids)), resource_type='audio-features')
        tr_resps = spotify.get_resources(
            ','.join(map(str, collected_ids)), resource_type='tracks')

    # create an array of processors with dataframes
    if "tracks" in tr_resps.keys():
        for i in range(len(tr_resps["tracks"])):
            processor = TrackFeatureProcessor(
                tr_resps["tracks"][i], af_resps["audio_features"][i], word)
            processor.process_feats_track()
            processor.extract_artists_df()
            processor.merge_track_features()
            processor.create_word_df()
            processors.append(processor)
    return processors


def spoti_search(word, spotify, collected_track_ids, prev_ids, offset=0, limit=20, global_limit=100, processors=[]):
    # most likely we will get several tracks per word,
    spotify_response = spotify.search(
        query=word, search_type="track", offset=offset, limit=limit)
    if "tracks" in spotify_response.keys():
        for track in spotify_response["tracks"]["items"]:
            # check if track_id is in master ID list
            if not track["id"] in prev_ids:
                collected_track_ids.append(track["id"])
    # add fresh ids to previous ids, !! Maybe shouldn't do it until have features
    prev_ids = prev_ids + collected_track_ids
    if (int(spotify_response["tracks"]["total"]) > int(spotify_response["tracks"]["offset"] + int(spotify_response["tracks"]["limit"]))) and (offset < global_limit):
        time.sleep(1)
        offset = offset + limit
        processors = populate_processors(spotify, word,
                                         processors, collected_track_ids)
        return spoti_search(word, spotify, collected_track_ids,
                            prev_ids, offset, limit, global_limit, processors=processors)
    else:
        return processors


def query_english():
    # lets get the random line from the library of all English words
    s = open("words.txt", "r")
    m = s.readlines()
    l = []
    for i in range(0, len(m) - 1):
        x = m[i]
        z = len(x)
        a = x[:z - 1]
        l.append(a)
    l.append(m[i + 1])
    o = random.choice(l)
    return o


def runmemore(spotify=SpotifyAPI(client_id, client_secret), q_words=["denial", "aggression"], track_requests_limit=200):
    processors = []

    # populate list of track ids
    previds = get_records(ALL_TRACKS, "id")
    # loop through random words to get tracks for each
    for word in q_words:
        processors = spoti_search(
            word, spotify, [], previds, global_limit=track_requests_limit)

    # merge all dataframes into one and save as CSV
    tracks_dfs = []
    artists_dfs = []
    word_df = []

    if len(processors) > 0:
        for processor in processors:
            tracks_dfs.append(processor.merged_df)
            artists_dfs.append(processor.artists_df)
            word_df.append(processor.word_df)

        tracks_df = pd.concat(tracks_dfs)
        artists_df = pd.concat(artists_dfs)
        words_df = pd.concat(word_df)

        if not path.exists(ALL_ARTISTS):
            artists_df.to_csv(ALL_ARTISTS, index=False)
        else:
            artists_df.to_csv(ALL_ARTISTS, mode='a', header=False, index=False)

        if not path.exists(ALL_TRACKS):
            tracks_df.to_csv(ALL_TRACKS, index=False)
        else:
            tracks_df.to_csv(ALL_TRACKS, mode='a', header=False, index=False)

        if not path.exists(ALL_WORDS):
            words_df.to_csv(ALL_WORDS, index=False)
        else:
            words_df.to_csv(ALL_WORDS, mode='a', header=False, index=False)


def random_word(num_runs):
    words = get_records(ALL_WORDS, "word")
    result = []
    for i in range(num_runs):
        word = query_english()
        # lets make sure we got a new word
        if word in words:
            while word in words:
                word = query_english()
        result.append(word)
    return result


words = ['we', 'hell', 'yes', 'she', 'like', 'breath', 'fire', 'don\'t', 'rock', 'disco', 'baby', 'twist', 'little', 'lonely']
runmemore(q_words=words, track_requests_limit=50)
# for i in range(0, 50):
#     words = random_word(1)
    # runmemore(q_words=words, track_requests_limit=50)  

def run_num_tracks(spotify=SpotifyAPI(client_id, client_secret), num_tracks=20, q_words=["denial", "aggression"], track_requests_limit=200):
    processors = []

    
    # loop through random words to get tracks for each
    for word in q_words:
        processors = spoti_search(
            word, spotify, [], [], global_limit=track_requests_limit, limit=num_tracks)

    # merge all dataframes into one and save as CSV
    user_tracks_dfs = []
    

    if len(processors) > 0:
        for processor in processors:
            user_tracks_dfs.append(processor.merged_df)
        

    return user_tracks_dfs
    
# my_list=run_num_tracks(spotify=SpotifyAPI(client_id, client_secret), num_tracks=10, q_words=["toxic"], track_requests_limit=10)
# print(my_list[0])