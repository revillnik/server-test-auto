from flask import Flask
from server_auto.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = "admin.login"
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from server_auto.main.views import main
    from server_auto.admin.views import admin

    app.register_blueprint(main)
    app.register_blueprint(admin)

    return app
