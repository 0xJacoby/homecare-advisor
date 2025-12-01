from typing import List, Optional, Tuple

from app.parameter.helper import format_bool, format_test
from app.person_info import PersonInfo


class Accessibility:
    # Optional ifall informationen inte finns, ksk inte så troligt för just age dock
    name = "Socialt Tillstånd"
    municipality: str
    has_home_care: Optional[bool]
    safety_alarm: Optional[bool]
    other_home_care: Optional[bool]
    social_network: Optional[bool]
    need_of_assistance: Optional[bool]
    personal_adl: Optional[bool]
    score: float
    incomplete = False

    def __init__(self, pi: PersonInfo):
        self.age = pi.age
        self.municipality = pi.municipality
        self.has_home_care = pi.has_home_care
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        
        acc_score = 0.1

        if self.has_home_care is True:
            return 1
        
        if self.safety_alarm is True:
            acc_score = acc_score + 1.0
        if self.other_home_care is True:
            acc_score = acc_score + 1.0
        if self.social_network is True:
            acc_score = acc_score + 1.0
        if self.need_of_assistance is not True:
            acc_score = acc_score + 1.0
        if self.personal_adl is True:
            acc_score = acc_score + 1.0
        
        
        return max((acc_score /  5.0), 1)


    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Kommun", self.municipality, str),
            format_test("Har hemhjälp", self.has_home_care, format_bool, True)
        ]