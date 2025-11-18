from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Database configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
        os.path.join(basedir, "database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Import and register routes
    from .api import patients, journals
    app.register_blueprint(patients, url_prefix="/api/patients")
    app.register_blueprint(journals, url_prefix="/api/journals")

    # Serve test gui
    @app.route("/")
    def index():
        return render_template("test_ui.html")

    return app
