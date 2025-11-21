from __future__ import annotations
from functools import reduce
import json
import operator
from typing import Any, Dict, List, Optional, Tuple
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()
root = os.getcwd()
config_path = root + "/config.json"

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

class PersonInfo:
    age: Optional[int]
    municipality: Optional[str]
    has_homecare: Optional[bool]

    def __init__(self, age, municipality, has_homecare):
        self.age = age
        self.municipality = municipality
        self.has_homecare = has_homecare

    def __repr__(self):
        return f"PersonInfo({self.age=}, {self.municipality=}, {self.has_homecare=})"
    # m.m

class Parameter:
    """Interface for parameters"""

    @classmethod
    def calculate_score(self) -> float:
        """
            Calculates score based on personal information and test values
            Returns a score in range [0, 1]
        """
        pass

class Accessibility(Parameter):
    age: Optional[int] # Optional ifall informationen inte finns, ksk inte så troligt för just age dock
    municipality: Optional[str]
    has_home_care: Optional[bool]
    def __init__(self, age: Optional[int], municipality: Optional[str], has_home_care: Optional[bool]):
        self.age = age
        self.municipality = municipality
        self.has_home_care = has_home_care

    @classmethod
    def calculate_score(self) -> float:
        if (self.has_home_care == None or self.has_home_care == False):
            return 0.0
        
        return self.decide_age() * self.decide_municipality()

    @classmethod
    def decide_age(self) -> float:
        """TODO: How to handle age"""
        
    @classmethod
    def decide_municipality(self) -> float:
        """TODO: How to handle municipality"""


class Category:
    name: str
    parameters: List[Tuple[Parameter, float]] # float is weight

    def __init__(self, name: str, parameters: List[Tuple[Parameter, float]]):
        self.name = name
        self.parameters = parameters

    @classmethod
    def combined_score(self) -> float:
        """Returns a score in the range [0, 1]"""
        reduce(operator.mul, map(Category.parameter_score, self))

    @staticmethod
    def parameter_score(parameter: Tuple[Parameter, float]):
        """Possible formula: Outputs a float in range [0, 1]\n
            Weight:
                If weight = 1 then score will not be weighted
                As weight -> 0: final_score -> 1 i.e. score matters less
                As weight -> inf: final_score -> 0 i.e. score matters more
            Score:
                If score = 1 then final_score = 1\n
                If score = 0 then final_score = 0 
            Drawbacks:
                \"Anomalies\" when score is very close to 1\n
                If score = 0.99 then weight needs to be around 25 for final_score to be (almost) 0\n
                If score = 0.9999 then weight needs to be around 250 for final_score to be (almost) 0
            Visual:
            https://www.desmos.com/calculator/j0krldwn5u
        """
        score = parameter[0].calculate_score()
        weight = parameter[1]

        return score ** (weight ** 2)
        """TODO: Change the formula"""
        parameter[0].calculate_score() * parameter[1]

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

class ParameterConfig:
    json: Any

    def __init__(self, parameter_obj):
        self.json = parameter_obj

    def name(self) -> str:
        return self.json["name"]

    def weight(self) -> float:
        return self.json["weight"]
    
    def set_weight(self, weight: float):
        self.json["weight"] = weight

    def print_me(self):
        print("ParameterConfig: { weight:", self.weight(), "}", end="")

class CategoryConfig:
    json: Any
    parameters: Dict[str, ParameterConfig]

    def __init__(self, category_obj):
        self.json = category_obj
        self.parameters = {}
        for parameter_obj in self.json["parameters"]:
            parameter = ParameterConfig(parameter_obj)
            self.parameters[parameter.name()] = parameter

    def name(self):
        return self.json["name"]

    def all_parameters(self) -> List[ParameterConfig]:
        return self.parameters.values()
    
    def add_parameter(self, parameter: str, weight: float):
        if parameter in self.parameters:
            self.remove_parameter(parameter)
        self.json["parameters"].append({
            "name" : parameter,
            "weight" : weight
        })
        self.parameters[parameter] = ParameterConfig(self.json["parameters"][-1])

    def remove_parameter(self, parameter: str):
        self.parameters.pop(parameter)
        for i in range(len(self.json['parameters'])):
            if self.json['parameters'][i]['name'] == parameter:
                self.json['parameters'].pop(i)

    def set_weight(self, parameter: str, weight: float):
        self.parameters[parameter].set_weight(weight)

    def print_me(self):
        print("CategoryConfig: { parameters : [", end="")
        for name in self.parameters:
            print(",\n\t", end="")
            print(name, ": ", end="")
            self.parameters[name].print_me()
        print('')
        print("]}")


class Config:
    """Innehållet i config.json"""
    json: Any
    categories: Dict[str, CategoryConfig]

    def __init__(self):
        self.categories = {}
        with open(config_path, 'r') as file:
            data = json.load(file)
            self.json = data
            for category_obj in data["categories"]:
                category = CategoryConfig(category_obj)
                self.categories[category.name()] = category

    def category_parameters(self, category_name: str) -> List[Tuple[str, float]]: # list of parameter name and weight
        return list(map(
            lambda x: (x.name(), x.weight()),
            self.categories[category_name].all_parameters()
        ))

    
    def set_weight(self, category: str, parameter: str, weight: float):
        self.categories[category].set_weight(parameter, weight)
        self.sync()

    def add_parameter(self, category: str, parameter: str, weight: float):
        self.categories[category].add_parameter(parameter, weight)
        self.sync()

    def remove_parameter(self, category: str, parameter: str):
        self.categories[category].remove_parameter(parameter)
        self.sync()

    def add_category(self, category: str):
        if category in self.categories:
            self.remove_category(category)
        self.json["categories"].append({
            "name" : category,
            "parameters" : []
        })
        self.categories[category] = CategoryConfig(self.json["categories"][-1])
        self.sync()

    def remove_category(self, category: str):
        self.categories.pop(category)
        for i in range(len(self.json['categories'])):
            if self.json['categories'][i]['name'] == category:
                self.json['categories'].pop(i)
        self.sync()


    def print_me(self):
        print("Config:")
        for name in self.categories:
            print(name ,": ", end="")
            self.categories[name].print_me()
            print("")

    def sync(self):
        with open(config_path, 'w') as file:
            file.write(json.dumps(self.json))



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

