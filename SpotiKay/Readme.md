# How to 

## Updating database:
python 
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:///spotitry_songs.db',echo=False)
base = declarative_base()
metadata = MetaData(engine, reflect=True)
table = metadata.tables.get("song")
base.metadata.drop_all(engine, [table], checkfirst=True)
df = pd.read_csv("all_tracks.csv")
df1 = df[["id","name","energy","liveness","danceability","instrumentalness","loudness","speechiness","valence","tempo"]]
df1.to_sql('song', con=engine, if_exists='append', index=False)