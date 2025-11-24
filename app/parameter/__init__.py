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

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """
        pass

    @staticmethod
    def from_name(name: str, pi: PersonInfo) -> Optional[Parameter]:
        match name:
            case "Accessibility":
                return Accessibility(pi)
            case "BloodPressure":
                return BloodPressure(pi)
            case "RespiratoryRate":
                return RespiratoryRate(pi)
            case "NEWS":
                return NEWS(pi)

        return None


