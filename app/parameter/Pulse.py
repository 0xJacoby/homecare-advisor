from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class Pulse:
    """Interface for parameters"""
    name = "Puls"
    pulse: Optional[float]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.pulse is None:
            self.incomplete = True
            return 1

        if self.pulse >= 110:
            return 0
        if self.pulse >= 100:
            return 1 / 3
        if self.pulse >= 90:
            return 2 / 3
        return 1

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Puls", self.pulse, str, True),
        ]