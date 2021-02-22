from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from myapp.extensions import db
from myapp.artifacts.utils import Encryption
from datetime import datetime
from passlib.hash import sha256_crypt
import os

ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# user registration fields wtforms
class CreateForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(max=30)])
    address = StringField('Address',validators=[DataRequired(),Length(max=30)])
    email = StringField('Email',validators=[Email('Invalid Email')])
    age = IntegerField('Age',validators=[DataRequired(),NumberRange(min=1,max=120)])
    likes_hobbies = StringField('Likes or hobbies',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(),Length(max=20)])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm',message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypted_name = db.Column(db.String(30))
    encrypted_address = db.Column(db.String(30))
    encrypted_email = db.Column(db.String(30))
    age = db.Column(db.Integer)
    encrypted_likes_hobbies = db.Column(db.String(30))
    encrypted_username =  db.Column(db.String(20))
    encrypted_password =  db.Column(db.String(100))
    profile_pic = db.Column(db.String(100))
    display = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.now)

    accounts = db.relationship('Accounts', backref='user', lazy=True)

    # getter and setter (encrypting values before saving to database)
    @property
    def name(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_name)
    @property
    def address(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_address)
    @property
    def email(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_email)
    @property
    def likes_hobbies(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_likes_hobbies)
    @property
    def username(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_username)
    @property
    def password(self):
      return self.encrypted_password
    
    @name.setter
    def name(self,value):
      self.encrypted_name = Encryption.encrypt(ENCRYPTION_KEY,value)
    @address.setter
    def address(self,value):
      self.encrypted_address = Encryption.encrypt(ENCRYPTION_KEY,value)
    @email.setter
    def email(self,value):
      self.encrypted_email = Encryption.encrypt(ENCRYPTION_KEY,value)
    @likes_hobbies.setter
    def likes_hobbies(self,value):
      self.encrypted_likes_hobbies = Encryption.encrypt(ENCRYPTION_KEY,value)
    @username.setter
    def username(self,value):
      self.encrypted_username = Encryption.encrypt(ENCRYPTION_KEY,value)
    @password.setter
    def password(self,value):
      self.encrypted_password = sha256_crypt.hash(value)


class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encrypted_social_media = db.Column(db.String(20))
    encrypted_username = db.Column(db.String(30))
    encrypted_password = db.Column(db.String(30))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    # getter and setter (encrypting values before saving to database)
    @property
    def social_media(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_social_media)
    @property
    def username(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_username)
    @property
    def password(self):
      return Encryption.decrypt(ENCRYPTION_KEY,self.encrypted_password)

    @social_media.setter
    def social_media(self,value):
      self.encrypted_social_media = Encryption.encrypt(ENCRYPTION_KEY,value)
    @username.setter
    def username(self,value):
      self.encrypted_username = Encryption.encrypt(ENCRYPTION_KEY,value)
    @password.setter
    def password(self,value):
      self.encrypted_password = Encryption.encrypt(ENCRYPTION_KEY,value)
