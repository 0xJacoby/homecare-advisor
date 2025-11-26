from typing import List, Optional, Tuple

from app.parameter.helper import format_bool, format_test
from app.person_info import PersonInfo


class Accessibility:
    # Optional ifall informationen inte finns, ksk inte så troligt för just age dock
    name = "Accessibility"
    age: int
    municipality: str
    has_home_care: Optional[bool]
    score: float
    incomplete = False

    def __init__(self, pi: PersonInfo):
        self.age = pi.age
        self.municipality = pi.municipality
        self.has_home_care = pi.has_home_care
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        if self.has_home_care is None or not self.has_home_care:
            self.incomplete = True
            return 0

        return self.decide_age() * self.decide_municipality()


    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Ålder", self.age, str),
            format_test("Kommun", self.municipality, str),
            format_test("Har hemhjälp", self.has_home_care, format_bool, True)
        ]

    def decide_age(self) -> float:
        """TODO: How to handle age"""

    def decide_municipality(self) -> float:
        """TODO: How to handle municipality"""
