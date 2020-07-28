# How to run
```
pipenv install
pipenv install pandas random-word requests 
python spotiparser.py
```

## To do
~~1. Exception handling for errors~~
   ~~1. Words are not found for Spotify~~
   ~~2. Random generator breaks~~
   ~~3. Empty arrays (maybe not a breaking bug however) ~~
~~2. Tame the random word generator so that it behaves itself.~~
~~3. Decide how to store this. ~~
   ~~1. Write a function that appends results to a master file.~~
4. Decide what part of runmemore() should become a Class / method

# Spotiparser Meldonium Edition (WADA non-compliant)

Uses random word from a 465k-word dictionary to find Spotify tracks, using pagination function of Spotify API.

## Steps
1. Pick desired <num_runs> of random words from ```random_word(num_runs)```
2. Use ```runmemore(spotify=SpotifyAPI(client_id, client_secret), q_words=<array of words>, track_requests_limit=<max number of tracks per word>)``` 
3. Search Spotify for tracks that use the words.
4. Return no more than ```track_requests_limit``` number of tracks
5. Add all the tracks to the master CSV files (defined as ```ALL_TRACKS```, ```ALL_ARTISTS```, ```ALL_WORDS```)

## How to run
```
pipenv install
pipenv install pandas requests 
python spotiparser_meldonium_edition.py
```