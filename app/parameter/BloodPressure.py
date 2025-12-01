from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class BloodPressure:
    """Interface for parameters"""
    name = "Blodtryck"
    systolic: Optional[float]
    diastolic: Optional[float]
    score: float
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        systolic_id = Tests.id_from_name("systolic")
        diastolic_id = Tests.id_from_name("diastolic")
        self.systolic = JournalEntry.latest_test_from_ssn(pi.ssn, systolic_id)
        self.diastolic = JournalEntry.latest_test_from_ssn(pi.ssn, diastolic_id)
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.systolic is None or self.diastolic is None:
            self.incomplete = True
            return 1

        if self.systolic < 120 and self.diastolic < 80:
            return 1
        elif (120 <= self.systolic < 130) and self.diastolic < 80:
            return 0.9
        elif (130 <= self.systolic < 140) or (80 <= self.diastolic < 90):
            return 0.7
        elif (140 <= self.systolic < 180) or (90 <= self.diastolic < 120):
            return 0.5
        else:
            return 0.1


    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Systoliskt", self.systolic, str, True),
            format_test("Diastoliskt", self.diastolic, str, True),
        ]