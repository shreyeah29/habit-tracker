import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Basic config
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{os.path.join(app.instance_path, 'habits.sqlite')}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Ensure instance folder exists (for SQLite file)
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    db.init_app(app)

    # Create DB tables on first run
    with app.app_context():
        from . import models
        db.create_all()

    # Register routes blueprint
    from .routes import bp
    app.register_blueprint(bp)

    return app
