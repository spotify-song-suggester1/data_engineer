""" SQLAlchemy models and utility functions"""

from flask_sqlalchemy import SQLAlchemy 
from sprs import DB
 
class Song(DB.Model):
    """Tracks"""
    id = DB.Column(DB.String(40), primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    energy = DB.Column(DB.Float, nullable=False)
    liveness = DB.Column(DB.Float, nullable=False)
    danceability = DB.Column(DB.Float, nullable=False)
    instrumentalness = DB.Column(DB.Float, nullable=False)
    loudness = DB.Column(DB.Float, nullable=False)
    speechiness = DB.Column(DB.Float, nullable=False)
    valence = DB.Column(DB.Float, nullable=False)
    tempo = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '[Song {}]'.format(self.name)
