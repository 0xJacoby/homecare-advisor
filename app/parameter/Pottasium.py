from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class Pottasium:
    """Interface for parameters"""
    name = "Kalium"
    pottasium: Optional[float]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        pottasium_id = Tests.id_from_name("pottasium")
        self.pottasium = JournalEntry.latest_test_from_ssn(pi.ssn, pottasium_id)
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.pottasium is None:
            self.incomplete = True
            return 1
        
        if 4 < self.pottasium < 4.5:
            return 1

        if 3.75 < self.pottasium < 4.75:
            return 2 / 3
        
        if 3.5 < self.pottasium < 5:
            return 1 / 3

        return 0

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Kalium", self.pottasium, str, True),
        ]