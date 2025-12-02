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

        crp_id = Tests.id_from_name("crp")

        crp_history = JournalEntry.get_tests_from_ssn(pi.ssn, crp_id, 2)

        self.current_crp = None
        self.old_crp = None

        if len(crp_history) >= 1:
            self.current_crp = crp_history[0]
        if len(crp_history) >= 2:
            self.old_crp = crp_history[1]

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