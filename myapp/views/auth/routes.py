from flask import Blueprint,render_template, url_for, redirect, flash, request, session
from myapp.extensions import db
from myapp.artifacts.models import User, CreateForm
from myapp.artifacts.utils import Encryption, is_unique
from passlib.hash import sha256_crypt
import os

auth = Blueprint('auth_blueprint',__name__)
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

@auth.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST' and 'user_id' not in session:
        username = request.form['username']
        encrypted_username = Encryption.encrypt(ENCRYPTION_KEY,request.form['username'])
        password = request.form['password']
        users = User.query.filter_by(encrypted_username=encrypted_username).all()
        for user in users:
          if username == user.username and sha256_crypt.verify(password,user.password):
              session['user_id'] = user.id
              flash('Hello  ' + user.name + '!','success')
              return redirect(url_for('dashboard_blueprint.user_dashboard')) 
        flash('Account not found. Try logging in again.', 'danger')         
        return render_template('content/login.html')
    session.pop('user_id', None)
    return render_template('content/login.html')


# register page
# password field uses sha256 encryption from passlib module
# the rest uses vigenere encryption (see artifacts/utils.py)
@auth.route('/create',methods=['POST','GET'])
def create():
    form = CreateForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if is_unique(form,User):
            user = User(
              name = form.name.data,
              address = form.address.data,
              email = form.email.data,
              age = form.age.data,
              likes_hobbies = form.likes_hobbies.data,
              username = form.username.data,
              password = form.password.data,
              profile_pic = 'profile.png',
              display = 1
            )
            db.session.add(user)
            db.session.commit()
            flash('Account successfully created!','success')
            return redirect(url_for('auth_blueprint.login'))
        else:
            flash('Password too weak! Try another one.','warning')
            render_template('content/create.html',form = form)
    return render_template('content/create.html',form = form)
