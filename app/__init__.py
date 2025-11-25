from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import os

"""
Utkast:
Application håller i config och databasen -- (Bör db variabeln också ligga där?)

1:
Kommer in en GET request

2:
Hämtar ssn:s

3: För varje ssn

    1:
    database.search_db(ssn) ger information:
        - om personen (det som inte ligger i journalen)
        - Alla relevanta categories

    2: För varje category

        1:
        config.category_parameters(self, category_name) ger namnen
            och vikterna på parametrarna

        2:
        parameter_from_name(person_info, database, name)
            vet vilken parameter som ska skapas och vilka
            fält som tas ut ur person_info och databasen
            baserat på namnet .

        3:
        category.combined_score() räknar ut score för specifika
        category.

    3:
    Minsta score returneras
"""

db = SQLAlchemy()
config = Config()


class Application(Flask):

    def __init__(self):
        super().__init__(__name__)

        # Initilize database
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "database.db"
        )
        self.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self)

        from app.api import register_routes

        # Register API routes
        register_routes(self)

        # Define non-API routes
        @self.route("/")
        def index():
            return render_template("test_ui.html")

        @self.route("/edit_category")
        def edit_category():
            return render_template("edit_category.html")

        @self.route("/add_category")
        def add_category():
            return render_template("add_category.html")

    @staticmethod
    def person_score(ssn: str):
        from app.models.categories import Categories

        categories = Categories.all_from_ssn(ssn)

        min_score = 1.0
        weights = []
        for category in categories:
            combined = category.combined_score()

            params = []
            for parameter, weight in config.categories[category.name].all_parameters().items():
                params.append(
                    {
                        "param": parameter,
                        "weight": weight.weight(),
                    }
                )

            weights.append(
                {
                    "name": category.name,
                    "value": combined,
                    "params": params,
                }
            )
            min_score = min(combined, min_score)

        return {
            "total": min_score,
            "categories": weights,
        }
