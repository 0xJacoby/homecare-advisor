from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class CRP:
    """Interface for parameters"""
    name = "CRP (C-reaktiv protein)"
    current_crp: Optional [float]
    old_crp: Optional [float]
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
        if self.current_crp or self.old_crp is None:
            self.incomplete = True
            return 1
        
        if self.old_crp - self.current_crp >= 15.0:
            return 1

        if self.old_crp - self.current_crp >= 10.0:
            return 0.8
        
        
        
        return 0.01

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("CRP", self.current_crp, str, True),
            format_test("Föregående CRP", self.old_crp, str, True)
        ]