from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Register blueprints
    from app.routes import main, auth, energy, water, waste, emissions, reports
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(energy.bp)
    app.register_blueprint(water.bp)
    app.register_blueprint(waste.bp)
    app.register_blueprint(emissions.bp)
    app.register_blueprint(reports.bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
