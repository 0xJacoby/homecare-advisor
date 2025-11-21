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