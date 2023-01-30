# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/explore', methods=['GET'])
@login_required
def explore():
    return render_template('explore.html', name=current_user.name, email=current_user.email, major=current_user.major)


#add path to view each user ID, if user is public annd current user is logged in
@main.route('/explore/<int:id>', methods=['GET'])
@login_required
def explore_id(id):
    user = User.query.get(id)
    if user.public == 'True':
        return render_template('explore_id.html', name=user.name, email=user.email, major=user.major, jobTitle=user.jobTitle, company=user.company, location=user.location, phone=user.phone, website=user.website, linkedin=user.linkedin, twitter=user.twitter)
    else:
        return render_template('explore.html', name=current_user.name, email=current_user.email, major=current_user.major)
