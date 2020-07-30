# How to 

## Updating database:
Assuming the imported file is all_tracks.csv

python 
from sqlalchemy import create_engine
engine = create_engine('sqlite:///spotitry_songs.db',echo=False)
df = pd.read_csv("all_tracks.csv")
df1 = df[["id","name","energy","liveness","danceability","instrumentalness","loudness","speechiness","valence","tempo"]]
df1.to_sql('song', con=engine, if_exists='append', index=False)
