from flask import Blueprint, request, session, jsonify
from myapp.extensions import db
from myapp.artifacts.models import User,Accounts
from passlib.hash import sha256_crypt
import os

api = Blueprint('api_blueprint',__name__,url_prefix='/api')
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# adds social media account information and encrypts it before storing to database
@api.route('/add',methods=['POST','GET'])
def accounts():
    if request.method == 'POST':
        social_media = request.form['social_media']
        username = request.form['username']
        password = request.form['password']
        account = Accounts(
          social_media=social_media,
          username=username,
          password=password,
          user_id=session['user_id']
        )
        db.session.add(account)
        db.session.commit()
    user = User.query.filter_by(id=session['user_id']).first()
    accounts = [
      {
        'id':account.id,
        'social_media':account.social_media,
        'username':account.username,
        'password':account.password,
      } 
      for account in user.accounts
    ]
    return jsonify(accounts)


@api.route('/delete',methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        Accounts.query.filter_by(id=request.form['id']).delete()
        db.session.commit()
        user = User.query.filter_by(id=session['user_id']).first()
        accounts = [
          {
            'id':account.id,
            'social_media':account.social_media,
            'username':account.username,
            'password':account.password,
          } 
          for account in user.accounts
        ]
        return jsonify(accounts)


@api.route('/edit',methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        account = Accounts.query.get(request.form['id'])
        account.social_media = request.form['social_media']
        account.username = request.form['username']
        account.password = request.form['password']
        db.session.commit()
        user = User.query.filter_by(id=session['user_id']).first()
        accounts = [
          {
            'id':account.id,
            'social_media':account.social_media,
            'username':account.username,
            'password':account.password,
          } 
          for account in user.accounts
        ]
        return jsonify(accounts)