from typing import Optional

from app.person_info import PersonInfo


class Accessibility:
    # Optional ifall informationen inte finns, ksk inte så troligt för just age dock
    age: Optional[int]
    municipality: Optional[str]
    has_home_care: Optional[bool]

    def __init__(self, pi: PersonInfo):
        self.age = pi.age
        self.municipality = pi.municipality
        self.has_home_care = pi.has_home_care

    def calculate_score(self) -> float:
        if self.has_home_care is None or not self.has_home_care:
            return 0.0

        return self.decide_age() * self.decide_municipality()

    def decide_age(self) -> float:
        """TODO: How to handle age"""

    def decide_municipality(self) -> float:
        """TODO: How to handle municipality"""
