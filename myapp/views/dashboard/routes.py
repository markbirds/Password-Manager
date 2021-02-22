from flask import Blueprint, render_template, session
from myapp.artifacts.models import User

dashboard = Blueprint('dashboard_blueprint',__name__)

#dashboard after user login
@dashboard.route('/dashboard')
def user_dashboard():
    #query all accounts stored based on user id in session
    #query all information of user to display in profile
    user = User.query.filter_by(id=session['user_id']).first()
    profile = {
      "id": user.id,
      "name": user.name,
      "address": user.address,
      "email": user.email,
      "age": user.age,
      "likes_hobbies": user.likes_hobbies,
      "profile_pic": "static/images/"+user.profile_pic,
      "display": user.display,
      "date_created_date": user.date_created.strftime("%B %d, %Y"),
      "date_created_hour": user.date_created.strftime("%I:%M %p")
    }
    accounts = user.accounts
    return render_template('content/dashboard.html',accounts = accounts,profile=profile)
