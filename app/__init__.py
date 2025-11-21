from __future__ import annotations
from functools import reduce
import json
import operator
from typing import Any, Dict, List, Optional, Tuple
from app.category import Category
from app.db import DB
from app.parameter import Parameter
from app.person_info import PersonInfo
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

class Application:
    database: DB
    config: Config

    def __init__(self):
        self.db = DB()
        self.config = Config()

    @classmethod
    def person_score(self, ssn: int):
        (person_info, category_names) = self.database.search_db(ssn)
        min_score = 1.0
        for category_name in category_names:
            parameter_names = self.config.category_parameters(self, category_name)
            parameters = list(map(
                lambda name: Application.parameter_from_name(person_info, self.database, name), 
                parameter_names
            ))
            category = Category(category_name, parameters)
            min_score = min(category.combined_score(), min_score)
        return min_score

    @staticmethod
    def parameter_from_name(person_info: PersonInfo, database: DB, parameter_name: Tuple[str, float]) -> Tuple[Parameter, float]:
        parameter = database.get_parameter(parameter_name[0], person_info)
        return (parameter, parameter_name[1])

