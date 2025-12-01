from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import os
from app.parameter.Accessibility import Accessibility
from app.parameter.BloodPressure import BloodPressure
from app.parameter.NEWS import NEWS
from app.parameter.RespiratoryRate import RespiratoryRate

from app.person_info import PersonInfo


class Parameter:
    """Interface for parameters"""
    name: str
    score: float
    incomplete = False # Set to true if there is not enough test data

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """
        pass

    @staticmethod
    def to_display_dict(cls: Parameter): # Static method to avoid having to implement for every class
        """
        Constructs a dict with the name, tests and score
        """
        
        return {
            "name": cls.name,
            "score": cls.score,
            "tests": [{
                    "name": name,
                    "value": value
                }
                for (name, value) in cls.tests()
            ],
            "incomplete": cls.incomplete
        }


    @staticmethod
    def from_name(name: str, pi: PersonInfo) -> Optional[Parameter]:
        match name:
            case "Accessibility":
                return Accessibility(pi)
            case "BloodPressure" | "Blodtryck":
                return BloodPressure(pi)
            case "RespiratoryRate":
                return RespiratoryRate(pi)
            case "NEWS":
                return NEWS(pi)

        return None


    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

