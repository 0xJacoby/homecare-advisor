from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class RespiratoryRate:
    """Interface for parameters"""
    name = "RespiratoryRate"
    age: int
    respiratory_rate: Optional[float]  # breaths per min
    score: float

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        self.age = pi.age
        respiratory_rate_id = Tests.id_from_name("respiratory_rate")
        self.respiratory_rate = JournalEntry.latest_test_from_ssn(pi.ssn, respiratory_rate_id)
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.respiratory_rate is None:
            return 0

        if self.age < 10:
            if 18 < self.respiratory_rate < 25:
                return 1
            else:
                return 0
        elif 10 <= self.age < 18:
            if 17 < self.respiratory_rate < 23:
                return 1
            else:
                return 0
        elif 18 <= self.age < 50:
            if 15 < self.respiratory_rate < 18:
                return 1
            else:
                return 0
        elif 50 <= self.age < 65:
            if 18 < self.respiratory_rate < 25:
                return 1
            else:
                return 0
        elif 65 <= self.age < 80:
            if 12 < self.respiratory_rate < 28:
                return 1
            else:
                return 0
        elif 80 <= self.age:
            if 10 < self.respiratory_rate < 30:
                return 1
            else:
                return 0
        return None


    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Ålder", self.age, str),
            format_test("Andningsfrekvens", self.respiratory_rate, str, True)
        ]