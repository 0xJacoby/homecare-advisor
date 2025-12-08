from typing import List, Optional, Tuple

from app.parameter.helper import format_bool, format_test, lerp_clamp
from app.person_info import PersonInfo


class NEWS:
    name = "NEWS"
    respiratory_rate: Optional[float]
    oxygen_saturation: Optional[float]
    supplied_oxygen: Optional[bool]
    systolic: Optional[float]
    pulse_frequency: Optional[float]
    temperature: Optional[float]
    score: float
    incomplete = False

    def __init__(self, pi: PersonInfo):
        from app.models.journal_entry import JournalEntry
        from app.models.tests import Tests

        respiratory_rate_id = Tests.id_from_name("respiratory_rate")
        oxygen_saturation_id = Tests.id_from_name("oxygen_saturation")
        supplied_oxygen_id = Tests.id_from_name("supplied_oxygen")
        systolic_id = Tests.id_from_name("systolic")
        pulse_frequency_id = Tests.id_from_name("pulse_frequency")
        temperature_id = Tests.id_from_name("temperature")
        self.respiratory_rate = JournalEntry.latest_test_from_ssn(
            pi.ssn, respiratory_rate_id
        )
        self.oxygen_saturation = JournalEntry.latest_test_from_ssn(
            pi.ssn, oxygen_saturation_id
        )
        self.supplied_oxygen = JournalEntry.latest_test_from_ssn(
            pi.ssn, supplied_oxygen_id
        )
        if not (self.supplied_oxygen is None):
            if self.supplied_oxygen == 0:
                self.supplied_oxygen = False
            else:
                self.supplied_oxygen = True
        self.systolic = JournalEntry.latest_test_from_ssn(pi.ssn, systolic_id)
        self.pulse_frequency = JournalEntry.latest_test_from_ssn(
            pi.ssn, pulse_frequency_id
        )
        self.temperature = JournalEntry.latest_test_from_ssn(
            pi.ssn, temperature_id)
        self.score = self.calculate_score()

    def calculate_score(self) -> float:
        """
        Calculates score based on personal information and test values
        Returns a score in range [0, 1]
        """

        if None in [
            self.respiratory_rate,
            self.oxygen_saturation,
            self.supplied_oxygen,
            self.systolic,
            self.pulse_frequency,
            self.temperature,
        ]:
            self.incomplete = True
            return 1

        individual = [
            self.respiratory_rate_score(),
            self.oxygen_saturation_score(),
            self.supplied_oxygen_score(),
            self.systolic_score(),
            self.pulse_frequency_score(),
            self.temperature_score(),
        ]

        news_score = sum(individual)
        possible = []
        if 3 in individual:
            possible.append(0.5)
        possible.append(1 - lerp_clamp(5, 12, news_score))
        return min(possible)

        if news_score == 0:
            possible.append(1)
        elif news_score <= 4:
            possible.append(0.75)
        elif news_score <= 6:
            possible.append(0.25)
        else:
            possible.append(0.0)
        print(possible)
        if not possible:
            return 0
        return min(possible)

    def tests(self) -> List[Tuple[str, str]]:
        """
        List of all test fields and their value (representation in str)
        If value is missing the it will be \"Missing\"
        """

        return [
            format_test("Andningsfrekvens", self.respiratory_rate, str, True),
            format_test("Syremättnad", self.oxygen_saturation, str, True),
            format_test("Tillförd syrgas", self.supplied_oxygen, format_bool, True),
            format_test("Systoliskt", self.systolic, str, True),
            format_test("Puls", self.pulse_frequency, str, True),
            format_test("Temperatur", self.temperature, str, True),
        ]

    def respiratory_rate_score(self) -> float:
        if self.respiratory_rate <= 8:
            return 3
        if self.respiratory_rate <= 11:
            return 1
        if self.respiratory_rate <= 20:
            return 0
        if self.respiratory_rate <= 24:
            return 2
        return 3

    def oxygen_saturation_score(self) -> float:
        if self.oxygen_saturation >= 96:
            return 0
        if self.oxygen_saturation >= 94:
            return 1
        if self.oxygen_saturation >= 92:
            return 2
        return 3

    def supplied_oxygen_score(self) -> float:
        if not self.supplied_oxygen:
            return 0
        return 2

    def systolic_score(self) -> float:
        if self.systolic <= 90:
            return 3
        if self.systolic <= 100:
            return 2
        if self.systolic <= 110:
            return 1
        if self.systolic <= 219:
            return 0
        return 3

    def pulse_frequency_score(self) -> float:
        if self.pulse_frequency <= 40:
            return 3
        if self.pulse_frequency <= 50:
            return 1
        if self.pulse_frequency <= 90:
            return 0
        if self.pulse_frequency <= 110:
            return 1
        if self.pulse_frequency <= 130:
            return 2
        return 3

    def temperature_score(self) -> float:
        if self.temperature <= 35:
            return 3
        if self.temperature <= 36:
            return 1
        if self.temperature <= 38:
            return 0
        if self.temperature <= 39:
            return 1
        return 2
