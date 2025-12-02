from .. import db
from typing import Any, Dict, List, Optional, Tuple


class JournalEntry(db.Model):
    __tablename__ = "journal_entries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_ssn = db.Column(
        db.String(13), db.ForeignKey("patients.ssn"), nullable=False
    )
    entry_date = db.Column(db.DateTime(timezone=True), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey("tests.id"), nullable=False)
    test_value = db.Column(db.Double, nullable=False)

    def __init__(self, patient_ssn, entry_date, test_id, test_value):
        self.patient_ssn = patient_ssn
        self.entry_date = entry_date
        self.test_id = test_id
        self.test_value = test_value

    def to_dict(self):
        return {
            "id": self.id,
            "patient_ssn": self.patient_ssn,
            "entry_date": self.entry_date,
            "test_id": self.test_id,
            "test_value": self.test_value,
        }

    @staticmethod
    def all_from_ssn(ssn):
        return JournalEntry.query.filter_by(patient_ssn=ssn).all()

    @staticmethod
    def get_tests_from_ssn(ssn, test_id, count) -> List[float]:
        tests = (
            JournalEntry.query.filter_by(patient_ssn=ssn, test_id=test_id)
                .order_by(JournalEntry.entry_date.desc())
                .limit(count)
        )

        return [t.test_value for t in tests]

    @staticmethod
    def latest_test_from_ssn(ssn, test_id, type = None) -> Optional[float]:
        test = (
            JournalEntry.query.filter_by(patient_ssn=ssn, test_id=test_id)
            .order_by(JournalEntry.entry_date.desc())
            .first()
        )

        if test:
            if type == "bool":
                if test.test_value == 0:
                    return False
                else:
                    return True
                
            return test.test_value
        else:
            return None
