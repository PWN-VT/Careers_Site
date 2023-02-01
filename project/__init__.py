# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pandas as pd

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWx83j4K4s82bciuCopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    from .models import Major

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

    #add csv file to database under major table
    
    def parseCSV(filePath):
        # CVS Column Names
        col_names = ['major', 'jobs']
        # Use Pandas to parse the CSV file
        csvData = pd.read_csv(filePath,names=col_names, header=None)
        # Loop through the rows in the CSV file
        for index, row in csvData.iterrows():
            # Create a Major object
            major = Major(major=row['major'], jobs=row['jobs'])
            # Add the major to the database
            db.session.add(major)

    with app.app_context():
        db.create_all()

    parseCSV('project/majors.csv')

    return app