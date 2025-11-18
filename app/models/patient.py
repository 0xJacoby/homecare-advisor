from .. import db


class Patient(db.Model):
    __tablename__ = "patients"

    ssn = db.Column(db.String(13), primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)

    journal_entries = db.relationship(
        "JournalEntry",
        backref="patient",
        lazy=True
    )

    def __init__(self, ssn, firstname="", surname=""):
        self.ssn = ssn
        self.firstname = firstname
        self.surname = surname

    def to_dict(self):
        return {
            "ssn": self.ssn,
            "firstname": self.firstname,
            "surname": self.surname
        }

    @staticmethod
    def from_ssn(ssn):
        return Patient.query.filter_by(ssn=ssn).first()
