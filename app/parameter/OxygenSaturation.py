from typing import List, Optional, Tuple

from app.parameter.helper import format_test, lerp_clamp
from app.person_info import PersonInfo


class OxygenSaturation:
    """Interface for parameters"""

    name = "Syregasmättnad"
    oxygen_saturation: Optional[float]
    target_saturation: Optional[float]
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        oxygen_saturation_id = Tests.id_from_name("oxygen_saturation")
        target_saturation_id = Tests.id_from_name("target_oxygen_saturation")
        self.oxygen_saturation = JournalEntry.latest_test_from_ssn(
            pi.ssn, oxygen_saturation_id
        )
        self.target_saturation = JournalEntry.latest_test_from_ssn(
            pi.ssn, target_saturation_id
        )
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if self.oxygen_saturation is None:
            self.incomplete = True
            return 1

        if not (self.target_saturation is None):
            if abs(self.oxygen_saturation - self.target_saturation) < 0.1:
                return 1
            else:
                return 0
        return lerp_clamp(92, 95, self.oxygen_saturation)

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Syregasmättnad", self.oxygen_saturation, str, True),
            format_test("Målmättnad", self.target_saturation, str, True),
        ]
