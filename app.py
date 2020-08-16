from flask import Flask, render_template, url_for, redirect, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, ValidationError, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from passlib.hash import sha256_crypt
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_mail import Mail,Message
import json
import Encryption
import os

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg'}
ENCRYPTION_KEY = 'JAHDFLKASDLKJFLKAJSDFLKJASNDLF'

app = Flask(__name__)
app.secret_key = 'Secret Key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'FALSE'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'flaskmail13579@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'flaskmail13579@gmail.com'
app.config['MAIL_PASSWORD'] = 'password_manager0329'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)

#login page
@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST' and 'account_id' not in session:
        username = request.form['username']
        password = request.form['password']
        accounts = AccountDetails.query.all()
        for account in accounts:
            if username == Encryption.decrypt(ENCRYPTION_KEY,account.username) and sha256_crypt.verify(password,account.password):
                session['account_id'] = account.account_id
                flash('Hello  '+Encryption.decrypt(ENCRYPTION_KEY,account.name)+'!','success')
                return redirect(url_for('dashboard')) 
        flash('Account not found. Try logging in again.', 'danger')         
        return render_template('login.html')
    session.pop('account_id', None)
    return render_template('login.html')

#account registration fields wtforms
class CreateForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(max=30)])
    address = StringField('Address',validators=[DataRequired(),Length(max=30)])
    email = StringField('Email',validators=[Email('Invalid Email')])
    age = IntegerField('Age',validators=[DataRequired(),NumberRange(min=1,max=120)])
    likes_hobbies = StringField('Likes or hobbies',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(),Length(max=20)])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Email')

#account_details table
class AccountDetails(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(30))
    email = db.Column(db.String(30))
    age = db.Column(db.Integer)
    likes_hobbies = db.Column(db.String(30))
    username =  db.Column(db.String(20))
    password =  db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))
    display = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now)

#accounts_stored table (stores social media accounts)
class Accounts_stored(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_media = db.Column(db.String(20))
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    account_id = db.Column(db.Integer)

#function to check if the username and password from registration form is unique in all accounts
def is_unique(form):
    accounts = AccountDetails.query.all()
    for account in accounts:
        if Encryption.decrypt(ENCRYPTION_KEY,account.username) == form.username.data and sha256_crypt.verify(form.password.data,account.password):
            return False
    return True

#register page
#password field uses sha256 encryption from passlib module
#the rest uses vigenere encryption (see Encryption.py)
#also stores default profile picture and default display for background
#returns false if the username and password is already in the database
@app.route('/create',methods=['POST','GET'])
def create():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if is_unique(form):
            name = Encryption.encrypt(ENCRYPTION_KEY,form.name.data)
            address = Encryption.encrypt(ENCRYPTION_KEY,form.address.data)
            email = Encryption.encrypt(ENCRYPTION_KEY,form.email.data)
            age = form.age.data
            likes_hobbies = Encryption.encrypt(ENCRYPTION_KEY,form.likes_hobbies.data)
            username = Encryption.encrypt(ENCRYPTION_KEY,form.username.data)
            password = sha256_crypt.hash(str(form.password.data)) 
            profile_pic = 'profile.png'
            display = 1
            user = AccountDetails(name=name,address=address,email=email,age=age,likes_hobbies=likes_hobbies,username=username,password=password,profile_pic=profile_pic,display=display)
            db.session.add(user)
            db.session.commit()
            flash('Account successfully created!','success')
            return redirect(url_for('login'))
        else:
            flash('Password too weak! Try another one.','warning')
            render_template('create.html',form = form)
    return render_template('create.html',form = form)

#dashboard after user login
@app.route('/dashboard')
def dashboard():
    #query all account stored based on account id in session
    #query all information of user to display in profile
    accounts = Accounts_stored.query.filter_by(account_id=session['account_id'])
    profile = AccountDetails.query.filter_by(account_id=session['account_id']).first()
    profile = {
    "id": session['account_id'],
    "name": Encryption.decrypt(ENCRYPTION_KEY,profile.name),
    "address": Encryption.decrypt(ENCRYPTION_KEY,profile.address),
    "email": Encryption.decrypt(ENCRYPTION_KEY,profile.email),
    "age": profile.age,
    "likes_hobbies": Encryption.decrypt(ENCRYPTION_KEY,profile.likes_hobbies),
    "profile_pic": "/static/images/"+profile.profile_pic,
    "display": profile.display,
    "date_created_date": profile.date_created.strftime("%B %d, %Y"),
    "date_created_hour": profile.date_created.strftime("%I:%M %p")
    }
    #edit_account and delete_account were used in function call in edit and delete button
    #both buttons takes the account id in accounts_stored table as argument
    id,social_media,username,password,edit_account,delete_account = [],[],[],[],[],[]
    for account in accounts:
        id.append(str(account.id))
        social_media.append(Encryption.decrypt(ENCRYPTION_KEY,account.social_media))
        username.append(Encryption.decrypt(ENCRYPTION_KEY,account.username))
        password.append(Encryption.decrypt(ENCRYPTION_KEY,account.password))
        edit_account.append('edit_account('+str(account.id)+')')
        delete_account.append('delete_account('+str(account.id)+')')
    accounts = zip(id,social_media,username,password,edit_account,delete_account)
    return render_template('dashboard.html',accounts = accounts,profile=profile)

#adds social media account information and encrypts it before storing to database
#also returns the new/current data in accounts_stored table in json format
@app.route('/accounts',methods=['POST','GET'])
def accounts():
    if request.method == 'POST':
        social_media = Encryption.encrypt(ENCRYPTION_KEY,request.form['social_media'])
        username = Encryption.encrypt(ENCRYPTION_KEY,request.form['username'])
        password = Encryption.encrypt(ENCRYPTION_KEY,request.form['password']) 
        account = Accounts_stored(social_media=social_media,username=username,password=password,account_id=session['account_id'])
        db.session.add(account)
        db.session.commit()
    accounts = Accounts_stored.query.filter_by(account_id=session['account_id'])
    query = []
    for account in accounts:
        query.append({
            "id": account.id,
            "social_media": Encryption.decrypt(ENCRYPTION_KEY,account.social_media),
            "username": Encryption.decrypt(ENCRYPTION_KEY,account.username),
            "password": Encryption.decrypt(ENCRYPTION_KEY,account.password),
            "edit_account_responsive": 'edit_account_responsive('+str(account.id)+')',
            "delete_account_responsive": 'delete_account_responsive('+str(account.id)+')'
        })
    return json.dumps(query)

#request for deletion of row and returns the current data in accounts_stored table
@app.route('/delete',methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        Accounts_stored.query.filter_by(id=request.form['id']).delete()
        db.session.commit()
        accounts = Accounts_stored.query.filter_by(account_id=session['account_id'])
        query = []
        for account in accounts:
            query.append({
                "id": account.id,
                "social_media": Encryption.decrypt(ENCRYPTION_KEY,account.social_media),
                "username": Encryption.decrypt(ENCRYPTION_KEY,account.username),
                "password": Encryption.decrypt(ENCRYPTION_KEY,account.password),
                "edit_account_responsive": 'edit_account_responsive('+str(account.id)+')',
                "delete_account_responsive": 'delete_account_responsive('+str(account.id)+')'
            })
        return json.dumps(query)

#edits the information in a row by using query.get()
#also returns all social media accounts stored in the database
@app.route('/edit',methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        account = Accounts_stored.query.get(request.form['id'])
        account.social_media = Encryption.encrypt(ENCRYPTION_KEY,request.form['social_media'])
        account.username = Encryption.encrypt(ENCRYPTION_KEY,request.form['username'])
        account.password = Encryption.encrypt(ENCRYPTION_KEY,request.form['password'])
        db.session.commit()
        accounts = Accounts_stored.query.filter_by(account_id=session['account_id'])
        query = []
        for account in accounts:
            query.append({
                "id": account.id,
                "social_media": Encryption.decrypt(ENCRYPTION_KEY,account.social_media),
                "username": Encryption.decrypt(ENCRYPTION_KEY,account.username),
                "password": Encryption.decrypt(ENCRYPTION_KEY,account.password),
                "edit_account_responsive": 'edit_account_responsive('+str(account.id)+')',
                "delete_account_responsive": 'delete_account_responsive('+str(account.id)+')'
            })
        return json.dumps(query)

#checks if there is a period in filename and it is in jpg format
#only allows images in jpg format    
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#route for uploading images
#copied from flask documentation
@app.route('/upload',methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','danger')
            return redirect(url_for('dashboard'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file','danger')
            return redirect(url_for('dashboard'))
        #setting filename based in the account id plus the original filename
        file.filename = 'profile_pic'+str(session['account_id'])+'_'+file.filename
        if file and allowed_file(file.filename):
            account = AccountDetails.query.get(session['account_id'])
            old_pic = 'static/images/'+account.profile_pic
            #check the photo already exists and it is not the default profile pic
            if os.path.exists(old_pic) and account.profile_pic != 'profile.png':
                os.remove(old_pic)  
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) 
            #updating the profile pic column in account_details tables
            account.profile_pic = filename    
            db.session.commit()
        return redirect(url_for('dashboard'))

#request of editing of personal information
@app.route('/personal_info', methods=['POST','GET'])
def personal_info():
    if request.method == 'POST':
        account = AccountDetails.query.get(request.form['id'])
        account.name = Encryption.encrypt(ENCRYPTION_KEY,request.form['name'])
        account.address = Encryption.encrypt(ENCRYPTION_KEY,request.form['address'])
        account.age = request.form['age']
        account.email = Encryption.encrypt(ENCRYPTION_KEY,request.form['email'])
        account.likes_hobbies = Encryption.encrypt(ENCRYPTION_KEY,request.form['likes_hobbies'])
        db.session.commit()
        return redirect(url_for('dashboard'))

#route for confirming if the old password was correct
#returns boolean expression
@app.route('/confirm_old_pass', methods=['POST','GET'])
def confirm_old_pass():
    account = AccountDetails.query.filter_by(account_id=session['account_id']).first()
    return json.dumps({
        'response': sha256_crypt.verify(request.form['old_pass'],account.password)
    })

#request for changing password
@app.route('/change_pass',methods=['POST','GET'])
def change_pass():
    if request.method == 'POST':
        account = AccountDetails.query.filter_by(account_id=session['account_id']).first()
        account.password = sha256_crypt.hash(str(request.form['new_pass'])) 
        db.session.commit()
        return redirect(url_for('dashboard'))

#request for changing background
@app.route('/save_display',methods=['POST','GET'])
def save_display():
    if request.method == 'POST':
        account = AccountDetails.query.filter_by(account_id=session['account_id']).first()
        account.display = request.form['display_number']
        db.session.commit()
        return redirect(url_for('dashboard'))

#function for sending mail through Flask Mail
@app.route('/mail/<send_type>',methods=['POST','GET'])
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
    return redirect(url_for('dashboard'))

#return a new format for dashboard if the screen width is less than 500
@app.route('/responsive')
def responsive():
    accounts = Accounts_stored.query.filter_by(account_id=session['account_id'])
    temp = []
    for account in accounts:
        temp.append({
            "id": str(account.id),
            "social_media": Encryption.decrypt(ENCRYPTION_KEY,account.social_media),
            "username": Encryption.decrypt(ENCRYPTION_KEY,account.username),
            "password": Encryption.decrypt(ENCRYPTION_KEY,account.password),
            "edit_account_responsive": 'edit_account_responsive('+str(account.id)+')',
            "delete_account_responsive": 'delete_account_responsive('+str(account.id)+')'
        })
    return json.dumps(temp)

if __name__ == '__main__':
    app.run(debug=True)