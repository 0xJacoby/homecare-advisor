from typing import List, Optional, Tuple

from app.parameter.helper import format_bool, format_test
from app.person_info import PersonInfo


class WishToStay:
    """Interface for parameters"""
    name = "Önskar stanna"
    wish_to_stay: Optional [bool]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        wish_to_stay_id = Tests.id_from_name("wish_to_stay")
        self.wish_to_stay = JournalEntry.latest_test_from_ssn(pi.ssn, wish_to_stay_id, "bool")
        
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """ 
        if self.wish_to_stay:
            return 0.5

        return 1

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Önskar att stanna", self.wish_to_stay, format_bool, True)
        ]