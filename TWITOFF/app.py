from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask (__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3' #config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title = 'Home', users=users)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title = 'Reset', users = [])


    #add in more stuff
    @app.route('/user',methods=['POST'])
    @app.route('/user/<name>',methods=['GET'])
    def user(name=None, message=''):
        #add this line in last:
        name = name or request.values['user_name']
        #import pdb; pdb.set_trace()
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name,e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
        message=message)

    #add in route for predictions
    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1, user2, request.values['tweet_text'])
            # prediction=predict_user(user1, user2, request.values['tweet_text'], CACHE)
            # CACHED_COMPARISONS.add((user1,user2))
            # CACHE.set('comparisons', dumps(CACHED_COMPARISONS))
            message = '"{}" is more likely to be said by {} than {}'.format(
                request.values['tweet_text'], user1 if prediction else user2,
                user2 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)


    return app
