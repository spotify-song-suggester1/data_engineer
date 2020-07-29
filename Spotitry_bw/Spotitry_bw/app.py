from os import getenv
from flask import Flask, render_template, request
from .models import DB, Song
from .predict import predict_best_songs
from .spotify import add_song

def create_app():
    """ Creates and configures a flask app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='Home')

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        song, artist = sorted([request.values['song_name'],
                               request.values['artist_name']])
        suggestions = predict_best_songs(song, artist)

        message = 'If you love {} by {}, we recommend: {}'.format(song, artist, suggestions)
               
        return render_template('recommendation.html', title='Recommendation',
                                message=message)
    
    return app