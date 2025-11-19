from functools import reduce
import operator
from typing import List, Optional, Tuple
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class PersonInfo:
    age: Optional[int]
    municipality: Optional[str]
    has_homecare: Optional[bool]

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
    age: Optional[int]
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
        from .api import patients, journals
        self.register_blueprint(patients, url_prefix="/api/patients")
        self.register_blueprint(journals, url_prefix="/api/journals")

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
        pass

class Config:
    @classmethod
    def category_parameters(self, category_name: str) -> List[Tuple[str, float]]: # list of parameter name and weight
        pass 


class Application:
    database: DB
    config: Config

    def __init__(self):
        self.db = DB()
        self.config = Config()

    @classmethod
    def person_score(self, ssn: int):
        (person_info, category_names) = self.database.search_db(ssn)
        min_score = 1
        for category_name in category_names:
            parameter_names = self.config.category_parameters(self, category_name)
            parameters = list(map(lambda name: Application.parameter_from_name(person_info, self.database, name), parameter_names))
            

    @staticmethod
    def parameter_from_name(person_info: PersonInfo, database: DB, parameter_name: Tuple[str, float]) -> Tuple[Parameter, float]:
        parameter = database.get_parameter(parameter_name[0], person_info)
        return (parameter, parameter_name[1])

