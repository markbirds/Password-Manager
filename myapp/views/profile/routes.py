from flask import Blueprint, url_for, redirect, flash, request, session, jsonify
from myapp.extensions import db, mail
from myapp.artifacts.models import User
from myapp.artifacts.utils import allowed_file
from passlib.hash import sha256_crypt
import os
from werkzeug.utils import secure_filename
from myapp.config.settings import UPLOAD_FOLDER
from flask_mail import Message

profile = Blueprint('profile_blueprint',__name__,url_prefix='/profile')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# route for uploading images
@profile.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','danger')
            return redirect(url_for('dashboard_blueprint.user_dashboard'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','danger')
            return redirect(url_for('dashboard_blueprint.user_dashboard'))
        #setting filename based in the account id plus the original filename
        file.filename = 'profile_pic'+str(session['user_id'])+'_'+file.filename
        if file and allowed_file(file.filename):
            account = User.query.get(session['user_id'])
            old_pic = UPLOAD_FOLDER+'/'+account.profile_pic
            # remove current profile pic
            if account.profile_pic != 'profile.png':
                os.remove(old_pic)  
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename)) 
            #updating the profile pic column in account_details tables
            account.profile_pic = filename    
            db.session.commit()
        return redirect(url_for('dashboard_blueprint.user_dashboard'))

#request of editing of personal information
@profile.route('/info', methods=['POST','GET'])
def info():
    if request.method == 'POST':
        user = User.query.get(request.form['id'])
        user.name = request.form['name']
        user.address = request.form['address']
        user.age = request.form['age']
        user.email = request.form['email']
        user.likes_hobbies = request.form['likes_hobbies']
        db.session.commit()
        return redirect(url_for('dashboard_blueprint.user_dashboard'))


@profile.route('/confirm_old_pass', methods=['POST','GET'])
def confirm_old_pass():
    account = User.query.filter_by(id=session['user_id']).first()
    return jsonify({
        'response': sha256_crypt.verify(request.form['old_pass'],account.password)
    })


@profile.route('/change_pass',methods=['POST','GET'])
def change_pass():
    if request.method == 'POST':
        user = User.query.filter_by(id=session['user_id']).first()
        user.password = sha256_crypt.hash(request.form['new_pass'])
        db.session.commit()
        return redirect(url_for('dashboard_blueprint.user_dashboard'))


@profile.route('/background',methods=['POST','GET'])
def background():
    if request.method == 'POST':
        user = User.query.filter_by(id=session['user_id']).first()
        user.display = request.form['display_number']
        db.session.commit()
        return redirect(url_for('dashboard_blueprint.user_dashboard'))

# sending mail through Flask Mail
@profile.route('/mail/<send_type>',methods=['POST','GET'])
def send_mail(send_type):
    if request.method == 'POST':
        if send_type == 'report':
            msg = Message('Problem from '+request.form['name'], recipients = ['flaskmail13579@gmail.com'])
            msg.body = request.form['report']
            mail.send(msg)
        if send_type == 'suggestion':
            msg = Message('Suggestion from '+request.form['name'], recipients = ['flaskmail13579@gmail.com'])
            msg.body = request.form['suggestion']
            mail.send(msg)
    return redirect(url_for('dashboard_blueprint.user_dashboard'))