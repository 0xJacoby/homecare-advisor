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
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        other_home_care_id = Tests.id_from_name("other_home_care")
        safety_alarm_id = Tests.id_from_name("safety_alarm")
        social_network_id = Tests.id_from_name("social_network")
        need_of_assistance_id = Tests.id_from_name("need_of_assistance")
        personal_adl_id = Tests.id_from_name("personal_adl")

        self.age = pi.age
        self.municipality = pi.municipality
        self.has_home_care = pi.has_home_care

        self.other_home_care = JournalEntry.latest_test_from_ssn(pi.ssn, other_home_care_id, "bool")
        self.safety_alarm = JournalEntry.latest_test_from_ssn(pi.ssn, safety_alarm_id, "bool")
        self.social_network = JournalEntry.latest_test_from_ssn(pi.ssn, social_network_id, "bool")
        self.need_of_assistance = JournalEntry.latest_test_from_ssn(pi.ssn, need_of_assistance_id, "bool")
        self.personal_adl = JournalEntry.latest_test_from_ssn(pi.ssn, personal_adl_id, "bool")

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
            format_test("Har hemhjälp", self.has_home_care, format_bool, True),
            format_test("Trygghetslarm", self.safety_alarm, format_bool, True),
            format_test("Har annan hemhjälp", self.other_home_care, format_bool, True),
            format_test("Socialt nätverk", self.social_network, format_bool, True),
            format_test("Behöver hemhjälp", self.need_of_assistance, format_bool, True),
            format_test("Personlig adl", self.personal_adl, format_bool, True),
        ]