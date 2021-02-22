from flask import Flask
from flask_bootstrap import Bootstrap
from .views.api.routes import api
from .views.auth.routes import auth
from .views.dashboard.routes import dashboard
from .views.profile.routes import profile
from .extensions import db, mail
from .commands import create_tables

def create_app(config_file='config/settings.py'):
  app = Flask(__name__)
  app.config.from_pyfile(config_file)
  Bootstrap(app)
  mail.init_app(app)
  db.init_app(app)
  app.register_blueprint(api)
  app.register_blueprint(auth)
  app.register_blueprint(profile)
  app.register_blueprint(dashboard)
  app.cli.add_command(create_tables)
  return app  


