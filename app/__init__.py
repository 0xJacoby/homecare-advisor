from random import random
from flask import Flask, render_template, jsonify
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
    @app.route("/test", methods=["GET"])
    def get_test_patients():
        resp = []
        for i in range(100):
            year = int(100 * random()) + 1920
            month = int(12 * random()) + 1
            date = int(30 * random()) + 1
            fyra_sista = int(10000 * random())
            dct = {
                "ssn": str(year)+str(month)+str(date)+str(fyra_sista),
                "age": 2025 - year,
                "firstname": "Johan",
                "surname": "Johansson",
                "score": random()
            }
            resp.append(dct)

        return jsonify(resp)

    return app
