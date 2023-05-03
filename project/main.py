# main.py
import os
from flask import Blueprint, render_template,request, send_from_directory, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import User
from . import db
import pandas as pd


#for helping find job titles by major: https://db.career.vt.edu/scripts/postgrad2006/report/EmployersJobTitlesLocationsList.asp?College=00&Major=ALL&Cohort=2016-2017&SortBy=M

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
#get current path + uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

#add favicon (Isnt working for some reason)
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@main.route('/profile')
@login_required
def profile():
    #log to docker logs
    print(current_user.profilePic)
    if current_user.student == '1':
        return render_template('profile.html', name=current_user.name, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio, profilePic=current_user.profilePic)
    else:
        return render_template('profile.html', name=current_user.name, email=current_user.email, major=current_user.major, jobTitle=current_user.jobTitle, company=current_user.company, location=current_user.location, phone=current_user.phone, website=current_user.website, bio=current_user.bio , linkedln=current_user.linkedln, twitter=current_user.twitter, profilePic=current_user.profilePic)

@main.route('/edit', methods=['GET'])
@login_required
def edit():
    if current_user.student == '1':
        return render_template('edit.html', name=current_user.name, profilePic=current_user.profilePic, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio, public=current_user.public)
    else:
        return render_template('edit.html', name=current_user.name, profilePic=current_user.profilePic, email=current_user.email, major=current_user.major, jobTitle=current_user.jobTitle, company=current_user.company, location=current_user.location, phone=current_user.phone, website=current_user.website, bio=current_user.bio , linkedln=current_user.linkedln, twitter=current_user.twitter, public=current_user.public)

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
    uploadPic = 1
    #see if the user uploaded a profile pic
    if 'profilePic' in request.files:
        #check if empty
        if request.files['profilePic'].filename == '':
            uploadPic = 0
        if uploadPic == 1:
            profilePic = request.files['profilePic']
            #if the user uploaded a profile pic, save it to the database
            if profilePic and allowed_file(profilePic.filename):
                filename = secure_filename(profilePic.filename)
                #check if there is already a file with the same name
                if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
                    #if there is, rename the uploaded file to a random hash
                    filename = os.path.splitext(filename)[0] + str(os.urandom(16).hex()) + os.path.splitext(filename)[1]
                    #update profile pic in database
                    current_user.profilePic = filename
                else:
                    #if not there, rename the uploaded file to a random hash
                    filename = os.path.splitext(filename)[0] + str(os.urandom(16).hex()) + os.path.splitext(filename)[1]
                    #update profile pic in database
                    current_user.profilePic = filename
                #save the file
                try: 
                    profilePic.save(os.path.join(UPLOAD_FOLDER, filename))
                except:
                    flash('Upload Error')
            else:
                flash('File type not allowed')
    
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
    #update the current users info in the database without adding a whole new user
    #updated_user = User(id=current_user.id, name=current_user.name, email=current_user.email, major=current_user.major, jobTitle=current_user.jobTitle, company=current_user.company, location=current_user.location, phone=current_user.phone, website=current_user.website, bio=current_user.bio, linkedln=current_user.linkedln, twitter=current_user.twitter, public=current_user.public, profilePic=current_user.profilePic)
    #update the user with the matching id in the database
    #db.session.merge(updated_user)
    #save changes to the sqllite database
    db.session.commit()
    #regrab the current user from the database
    current_user2 = User.query.filter_by(id=current_user.id).first()
    #remove parts of this
    flash('Your changes have been saved.')

    if current_user.student == '1':
        return render_template('edit.html', name=current_user2.name, profilePic=current_user2.profilePic , email=current_user2.email, major=current_user2.major, location=current_user2.location, phone=current_user2.phone, website=current_user2.website, linkedln=current_user2.linkedln, twitter=current_user2.twitter, bio=current_user2.bio, public=current_user2.public)
    else:
        return render_template('edit.html', name=current_user2.name, profilePic=current_user2.profilePic , email=current_user2.email, major=current_user2.major, jobTitle=current_user2.jobTitle, company=current_user2.company, location=current_user2.location, phone=current_user2.phone, website=current_user2.website, bio=current_user2.bio , linkedln=current_user2.linkedln, twitter=current_user2.twitter, public=current_user2.public)

    

@main.route('/explore', methods=['GET'])
@login_required
def explore():
    #add csv file to a table on the page under major table
    def parseCSV(filePath):
        df = pd.read_csv(filePath)
        return df #could also return df.to_html() for a table of everything
    if current_user.student == '1':
        majorJobs = parseCSV('project/majors.csv')
        #grab the rows with the same major as the current user
        majorJobs2 = majorJobs.loc[majorJobs['Major'] == current_user.major]
        #save variables of the job name, company, and link
        majorJobs3 = majorJobs2[['Title', 'Company', 'Link']]
        #convert to a list
        majorJobs3 = majorJobs3.values.tolist()
        return render_template('explore.html', majorJobs=majorJobs3, id=current_user.id, name=current_user.name, email=current_user.email, major=current_user.major, location=current_user.location, phone=current_user.phone, website=current_user.website, linkedln=current_user.linkedln, twitter=current_user.twitter, bio=current_user.bio, users = User.query.all(), student=current_user.student, profilePic=current_user.profilePic)
    return render_template('explore.html', id=current_user.id, name=current_user.name, email=current_user.email, major=current_user.major, users = User.query.all(), student=current_user.student, profilePic=current_user.profilePic)


#add path to view each user ID, if user is public annd current user is logged in
@main.route('/explore/<int:id>', methods=['GET'])
@login_required
def explore_id(id):
    try:
        user = User.query.get(id)
    except:
        return render_template('error.html')
    if user.public == '1':
        return render_template('explore_id.html', name=user.name, email=user.email, major=user.major, jobTitle=user.jobTitle, company=user.company, location=user.location, phone=user.phone, website=user.website, linkedln=user.linkedln, twitter=user.twitter)
    else:
        return render_template('explore.html', name=current_user.name, email=current_user.email, major=current_user.major)

@main.route('/uploads//<string:id>', methods=['GET'])
@login_required
def uploads(id):
    #get the file name from uploads/<file name>
    file = id
    #get the file path
    path = os.path.join(main.root_path, 'uploads', file)
    #return the file
    return send_file(path, as_attachment=True)

@main.route('/admin', methods=['GET'])
@login_required
def admin():
    if current_user.admin == '1':
        #get line count of select * from users
        usercount = db.session.query(User).count()
        return render_template('admin.html', name = current_user.name,userCount = usercount)
    else:
        return render_template('error.html')
