# from flask import Flask
# from config import Config
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
# from flask_debugtoolbar import DebugToolbarExtension

# app = Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# login = LoginManager(app)
# login.login_view = 'login'

# from app import main, models
# DebugToolbarExtension(app)

from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'main.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.club import bp as club_bp
    app.register_blueprint(club_bp)

    from app.courts import bp as courts_bp
    app.register_blueprint(courts_bp)

    from app.leagues import bp as leagues_bp
    app.register_blueprint(leagues_bp)

    from app.flights import bp as flights_bp
    app.register_blueprint(flights_bp)

    from app.players import bp as players_bp
    app.register_blueprint(players_bp)

    from app.scheduler import bp as scheduler_bp
    app.register_blueprint(scheduler_bp)

    from app.timeslots import bp as timeslots_bp
    app.register_blueprint(timeslots_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
