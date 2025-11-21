from __future__ import annotations
from functools import reduce
import json
import operator
from typing import Any, Dict, List, Optional, Tuple
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
root = os.getcwd()
config_path = root + "/config.json"

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
