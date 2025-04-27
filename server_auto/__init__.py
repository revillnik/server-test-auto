from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = "admin.login"

app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)

from server_auto.views import *

from .admin.views import admin

app.register_blueprint(admin)
