from typing import List, Optional, Tuple

from app.parameter.helper import format_test
from app.person_info import PersonInfo


class BodyTemperature:
    """Interface for parameters"""
    name = "Kroppstemperatur"
    temperature: Optional [float]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        temperature_id = Tests.id_from_name("temperature")
        self.temperature = JournalEntry.latest_test_from_ssn(pi.ssn, temperature_id)

        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.temperature is None:
            self.incomplete = True
            return 1
        
        if 36.0 <= self.temperature <= 37.8:
            return 1

        return 0

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Kroppstemperatur", self.temperature, str, True)
        ]