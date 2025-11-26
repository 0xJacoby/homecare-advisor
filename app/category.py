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
from app import config
import os


class Category:
    name: str
    parameters: List[Tuple[Parameter, float]]  # float is weight
    score: float

    def __init__(self, name: str, parameters: List[Tuple[Parameter, float]]):
        self.name = name
        self.parameters = parameters
        self.score = self.combined_score()

    def combined_score(self) -> float:
        """Returns a score in the range [0, 1]"""
        return reduce(operator.mul, map(Category.parameter_score, self.parameters), 1)

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

        return score ** (weight**2)
        """TODO: Change the formula"""
        parameter[0].calculate_score() * parameter[1]

    def to_dict(self):
        return config.get_category(self.name).to_dict()
    
    def to_display_dict(self):
        return {
            "name": self.name,
            "score": self.score,
            "parameters": [
                Category.display_add_weight(
                    Parameter.to_display_dict(parameter), 
                    weight
                ) for (parameter, weight) in self.parameters
            ]
                
        }

    @staticmethod
    def from_name(name: str, pi: PersonInfo):
        return Category(name, config.category_parameters(name, pi))

    @staticmethod
    def display_add_weight(parameter_dict, weight: float):
        parameter_dict["weight"] = weight
        return parameter_dict