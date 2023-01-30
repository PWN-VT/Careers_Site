# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    jobTitle = db.Column(db.String(1000))
    bio = db.Column(db.String(1000))
    company = db.Column(db.String(1000))
    location = db.Column(db.String(1000))
    phone = db.Column(db.String(1000))
    website = db.Column(db.String(1000))
    linkedin = db.Column(db.String(1000))
    twitter = db.Column(db.String(1000))
    public = db.Column(db.String(100))
    major = db.Column(db.String(1000))
    student = db.Column(db.String(100))