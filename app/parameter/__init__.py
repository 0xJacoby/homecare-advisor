from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
import os
from app.parameter.CRP import CRP
from app.parameter.Accessibility import Accessibility
from app.parameter.BloodPressure import BloodPressure
from app.parameter.BodyTemperature import BodyTemperature
from app.parameter.EGFR import EGFR
from app.parameter.Glucose import Glucose
from app.parameter.Hemoglobin import Hemoglobin
from app.parameter.Krea import Krea
from app.parameter.LPK import LPK
from app.parameter.NEWS import NEWS
from app.parameter.OxygenSaturation import OxygenSaturation
from app.parameter.Pottasium import Pottasium
from app.parameter.Pulse import Pulse
from app.parameter.RespiratoryRate import RespiratoryRate

from app.parameter.Sodium import Sodium
from app.parameter.TPK import TPK
from app.parameter.WishToStay import WishToStay
from app.person_info import PersonInfo


class Parameter:
    """Interface for parameters"""

    name: str
    score: float
    incomplete = False  # Set to true if there is not enough test data

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """
        pass

    @staticmethod
    def to_display_dict(
        cls: Parameter,
    ):  # Static method to avoid having to implement for every class
        """
        Constructs a dict with the name, tests and score
        """

        return {
            "name": cls.name,
            "score": cls.score,
            "tests": [{"name": name, "value": value} for (name, value) in cls.tests()],
            "incomplete": cls.incomplete,
        }

    @staticmethod
    def from_name(name: str, pi: PersonInfo) -> Optional[Parameter]:
        match name:
            case "Socialt Tillstånd":
                return Accessibility(pi)
            case "Blodtryck":
                return BloodPressure(pi)
            case "Kroppstemperatur":
                return BodyTemperature(pi)
            case "CRP (C-reaktiv protein)":
                return CRP(pi)
            case "eGFR":
                return EGFR(pi)
            case "Andningsfrekvens":
                return RespiratoryRate(pi)
            case "NEWS":
                return NEWS(pi)
            case "Glukos":
                return Glucose(pi)
            case "Hemoglobin (Hb)":
                return Hemoglobin(pi)
            case "Krea":
                return Krea(pi)
            case "LPK":
                return LPK(pi)
            case "Syremättnad" | "Syrem\u00e4ttnad":
                return OxygenSaturation(pi)
            case "Kalium":
                return Pottasium(pi)
            case "Puls":
                return Pulse(pi)
            case "Natrium":
                return Sodium(pi)
            case "TPK":
                return TPK(pi)
            case "Önskar stanna":
                return WishToStay(pi)
        print("ERROR: Parametern: ", name, " saknas")

        return None

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """
