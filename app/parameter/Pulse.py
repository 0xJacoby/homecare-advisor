from typing import List, Optional, Tuple

from app.parameter.helper import format_test, lerp_clamp
from app.person_info import PersonInfo


class Pulse:
    """Interface for parameters"""
    name = "Puls"
    pulse: Optional[float]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        pulse_id = Tests.id_from_name("pulse_frequency")
        self.pulse = JournalEntry.latest_test_from_ssn(pi.ssn, pulse_id)
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.pulse is None:
            self.incomplete = True
            return 1
        return 1 - lerp_clamp(90, 110, self.pulse)

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Puls", self.pulse, str, True),
        ]