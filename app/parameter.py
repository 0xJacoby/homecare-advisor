from __future__ import annotations
from functools import reduce
import json
import operator
from typing import Any, Dict, List, Optional, Tuple
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.config import Config
import os

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
