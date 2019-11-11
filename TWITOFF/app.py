from flask import Flask
from .models import DB 

# now we want to make an app factory

def create_app():
    app = Flask(__name__)

    #add our config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    #now let the database know about the app
    DB.init_app(app)

    @app.route('/')
    def root():
            return 'Welcome to Twitoff!'
    return app        