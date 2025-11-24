from __future__ import annotations

from typing import Optional
from datetime import datetime


class PersonInfo:
    ssn: int
    age: Optional[int]
    municipality: Optional[str]
    has_homecare: Optional[bool]

    def __init__(self, ssn: str):
        from app.models.patient import Patient

        patient = Patient.from_ssn(ssn)

        self.ssn = ssn
        self.age = datetime.now().year - int(ssn[0:4])
        self.municipality = patient.municipality
        self.has_homecare = patient.has_homecare

    def __repr__(self):
        return f"PersonInfo({self.age=}, {self.municipality=}, {self.has_homecare=})"

    # m.m
