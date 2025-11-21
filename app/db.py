from __future__ import annotations
from functools import reduce
import json
import operator
from typing import Any, Dict, List, Optional, Tuple
from app.parameter import Parameter
from app.person_info import PersonInfo
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.config import Config
import os

db = SQLAlchemy()

class DB(Flask):
    def __init__(self):
        super().__init__(__name__)

        # Database configuration
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + \
            os.path.join(basedir, "database.db")
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.init_app(self)

        # Import and register routes
        from .api import patients, journals, categories, tests
        self.register_blueprint(patients, url_prefix="/api/patients")
        self.register_blueprint(journals, url_prefix="/api/journals")
        self.register_blueprint(categories, url_prefix="/api/categories")
        self.register_blueprint(tests, url_prefix="/api/tests")

        # Serve test gui
        @self.route("/")
        def index():
            return render_template("test_ui.html")

    @classmethod
    def get_parameter(self, id: str, pi: PersonInfo) -> Optional[Parameter]:
        match id:
            case "Accessibility":
                pass
        return None

    @classmethod
    def search_db(self, ssn: int) -> Tuple[PersonInfo, List[str]]: # List of category names
        from app.models.patient import Patient
        from app.models.categories import Categories
        from app.models.journal_entry import JournalEntry

        patient = Patient.from_ssn(ssn)
        person_info = PersonInfo(
            age=divmod((datetime.now() - patient.date_of_birth).total_seconds(), 31536000)[0],
            municipality=patient.municipality,
            has_homecare=patient.has_homecare,
        )

        data = (db.session.query(JournalEntry, Categories)
                .filter_by(ssn=ssn)
                .filter_by(test_id = 1)
                .join(Categories, Categories.id == JournalEntry.test_value, isouter=True)
                .all())

        categories = [c.name for _, c in data]
        return (person_info, categories)
