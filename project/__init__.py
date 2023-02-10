# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OtWx83j4K4s82bciuCNpO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()
        #add users to database for testing
        user1 = User(name='test', email='test@test.com', major='test', jobTitle='', company='', location='test', phone='test', website='test', bio='test', linkedln='test', twitter='test', public='1', student='1', password=generate_password_hash('test', method='sha256'))
        user2 = User(name='test2', email='test2@test.com', major='test', jobTitle='test', company='test', location='test', phone='test', website='test', bio='test', linkedln='test', twitter='test', public='1', student='0', password=generate_password_hash('test', method='sha256'))
        #add users to database
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    
    return app