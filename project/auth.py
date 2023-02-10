# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db
import os

auth = Blueprint('auth', __name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#get current path + uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():

    #get uploaded profile pic
    profilePic = request.files['profilePic']
    email = request.form.get('email')
    name = request.form.get('name')
    bio = request.form.get('bio')
    password = request.form.get('password')
    jobTitle = request.form.get('jobTitle')
    company = request.form.get('company')
    location = request.form.get('location')
    phone = request.form.get('phone')
    website = request.form.get('website')
    linkedln = request.form.get('linkedln')
    twitter = request.form.get('twitter')
    major = request.form.get('major')
    public = request.form.get('public')
    if public == 'on':
        public = True
    else:
        public = False

    student = False
    #check if bio is longer than 1000 chars
    if len(bio) > 1000:
        flash('Bio is too long')
        return redirect(url_for('auth.signup'))

    #check if profilePic is an image
    if profilePic.filename == '':
        flash('No selected file')
        return redirect(url_for('auth.signup'))
    if profilePic and allowed_file(profilePic.filename):
        filename = secure_filename(profilePic.filename)
        profilePic.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        flash('File type not allowed')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), student=student, bio=bio, jobTitle=jobTitle, company=company, location=location, phone=phone, website=website, linkedln=linkedln, twitter=twitter, public=public, major=major, profilePic=filename)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/studentSignup')
def studentSignup():
    return render_template('studentSignup.html')

@auth.route('/studentSignup', methods=['POST'])
def studentSignup_post():

    profilePic = request.files['profilePic']
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    bio = request.form.get('bio')
    location = request.form.get('location')
    phone = request.form.get('phone')
    website = request.form.get('website')
    linkedln = request.form.get('linkedln')
    twitter = request.form.get('twitter')
    major = request.form.get('major')
    public = request.form.get('public')
    gradYear = request.form.get('gradYear')
    if public == 'on':
        public = True
    else:
        public = False

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    student = True
    #check if bio is longer than 1000 chars
    if len(bio) > 1000:
        flash('Bio is too long')
        return redirect(url_for('auth.signup'))

    #check if profilePic is an image
    if profilePic.filename == '':
        flash('No selected file')
        return redirect(url_for('auth.signup'))
    if profilePic and allowed_file(profilePic.filename):
        filename = secure_filename(profilePic.filename)
        profilePic.save(os.path.join(UPLOAD_FOLDER, filename))
    else:
        flash('File type not allowed')
        return redirect(url_for('auth.signup'))

    if user: # if a user is found, we want to redirect back to signup page so user can try again  
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), student=student, bio=bio, location=location, phone=phone, website=website, linkedln=linkedln, twitter=twitter, public=public, major=major, profilePic=filename)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))