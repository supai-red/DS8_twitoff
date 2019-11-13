"""These are my database models"""

from flask_sqlalchemy import SQLAlchemy
#this file is for the schema

#import database. capital for global scope
DB = SQLAlchemy()

class User(DB.Model):
    """Twitter users that we analyze"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Tweet(DB.Model):
    """The user's tweets from twitter"""
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    #DB.relationship is used in place of DB.Column to back reference to another column
    #The above 2 lines establish the one-many relationship between users and tweets

    embedding = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
       return '<Tweet {}>'.format(self.text)