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
        user1 = User(name='Example User', email='test@test.com', major='Cybersecurity MGT', jobTitle='', company='', location='111-111-1111', phone='test', website='test.com', bio='testing', linkedln='test', twitter='test', public='1', student='1', admin='0', password=generate_password_hash('test', method='sha256'))
        user2 = User(name='Example User 2', email='test2@test.com', major='Cybersecurity MGT', jobTitle='Security Engineer', company='Example Company', location='Blacksburg, VA', phone='111-111-1111', website='test.com', bio='testing', linkedln='test', twitter='test', public='1', student='0', admin='0', password=generate_password_hash('test', method='sha256'))
        user3 = User(name='admin', email='admin@admin.com', major='Cybersecurity MGT', jobTitle='Security Engineer', company='Example Company', location='Blacksburg, VA', phone='111-111-1111', website='test.com', bio='testing', linkedln='test', twitter='test', public='0', student='0', admin='1', password=generate_password_hash('projectmgt', method='sha256'))
        #add users to database
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.query(User).filter(User.email == 'anthony@prettyprinted.com').delete()
        db.session.query(User).filter(User.email == 'anthony@gmail.com').delete()
        db.session.commit()
    
    return app