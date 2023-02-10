# main.py
import os
from flask import Blueprint, render_template,request, send_from_directory, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User
import pandas as pd

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

#add favicon
@main.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/profile')
@login_required
def profile():
    if current_user.student == '1':
        return render_template('profile.html', name=current_user.name, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio)
    else:
        return render_template('profile.html', name=current_user.name, email=current_user.email, major=current_user.major, jobTitle=current_user.jobTitle, company=current_user.company, location=current_user.location, phone=current_user.phone, website=current_user.website, bio=current_user.bio , linkedln=current_user.linkedln, twitter=current_user.twitter)

@main.route('/edit', methods=['GET'])
@login_required
def edit():
    if current_user.student == '1':
        return render_template('edit.html', name=current_user.name, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio, public=current_user.public)
    else:
        return render_template('edit.html', name=current_user.name, email=current_user.email, major=current_user.major, jobTitle=current_user.jobTitle, company=current_user.company, location=current_user.location, phone=current_user.phone, website=current_user.website, bio=current_user.bio , linkedln=current_user.linkedln, twitter=current_user.twitter, public=current_user.public)

@main.route('/edit', methods=['POST'])
@login_required
def edit_post():
    #get user info from form
    name = request.form.get('name')
    email = request.form.get('email')
    major = request.form.get('major')
    jobTitle = request.form.get('jobTitle')
    location = request.form.get('location')
    phone = request.form.get('phone')
    website = request.form.get('website')
    bio = request.form.get('bio')
    linkedln = request.form.get('linkedln')
    twitter = request.form.get('twitter')
    public = request.form.get('public')
    
    if current_user.student == 'True':
        company = ''
    else:
        company = request.form.get('company')

    if len(bio) > 1000:
        flash('Bio is too long')
        return redirect(url_for('main.edit'))

    #update user info
    current_user.name = name
    current_user.email = email
    current_user.major = major
    current_user.jobTitle = jobTitle
    current_user.company = company
    current_user.location = location
    current_user.phone = phone
    current_user.website = website
    current_user.bio = bio
    current_user.linkedln = linkedln
    current_user.twitter = twitter
    current_user.public = public
    

@main.route('/explore', methods=['GET'])
@login_required
def explore():
    #add csv file to a table on the page under major table
    def parseCSV(filePath):
        df = pd.read_csv(filePath)
        return df #could also return df.to_html() for a table of everything
    if current_user.student == '1':
        majorJobs = parseCSV('project/majors.csv')
        #pick out the row with the major in it
        majorJobs2 = majorJobs.loc[majorJobs['major'] == current_user.major]
        #parse the jobs column into a list, it contains multiple jobs seperated by "|"
        majorJobs3 = majorJobs['jobs'].values[0].split('|')
        return render_template('explore.html', majorJobs=majorJobs3, id=current_user.id, name=current_user.name, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio, users = User.query.all())
    return render_template('explore.html', id=current_user.id, name=current_user.name, email=current_user.email, major=current_user.major, users = User.query.all())


#add path to view each user ID, if user is public annd current user is logged in
@main.route('/explore/<int:id>', methods=['GET'])
@login_required
def explore_id(id):
    user = User.query.get(id)
    if user.public == '1' and user.student == '0':
        return render_template('explore_id.html', name=user.name, email=user.email, major=user.major, jobTitle=user.jobTitle, company=user.company, location=user.location, phone=user.phone, website=user.website, linkedln=user.linkedln, twitter=user.twitter)
    else:
        return render_template('explore.html', name=current_user.name, email=current_user.email, major=current_user.major)
