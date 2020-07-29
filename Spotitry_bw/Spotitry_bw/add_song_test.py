from spotify import get_features, add_song, track_id_for_artist_title
import sqlite3

conn = sqlite3.connect('spotitry_songs.db')
curs = conn.cursor()

track_id = track_id_for_artist_title('coheed and cambria', 'the suffering')

song_predict = get_features(track_id)

add_song(song_predict)

print(curs.rowcount, 'was inserted.')

