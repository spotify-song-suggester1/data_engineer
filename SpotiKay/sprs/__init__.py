rom os import getenv
from flask import Flask, render_template, request

from sqlalchemy_utils import database_exists
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
DB = SQLAlchemy(app)

from .models import Song
from .predict import predict_best_songs
from .spotify import add_song


def create_app():
    """ Creates and configures a flask app"""

    if not database_exists(getenv('DATABASE_URL')):
        DB.drop_all()
        DB.create_all()    
    return app

@app.route('/')
def root():
    return render_template('base.html', title='Home')

@app.route('/compare', methods=['POST'])
def compare(message=''):
    song, artist = [request.values['song_name'],
                            request.values['artist_name']]
    suggestions = predict_best_songs(song, artist)

    message = 'If you love {} by {}, we recommend: {}'.format(song, artist, ' or '.join(map(str, suggestions)))
            
    return render_template('recommendation.html', title='Recommendation',
                            message=message)