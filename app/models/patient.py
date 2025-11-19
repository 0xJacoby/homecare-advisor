from .. import db


class Patient(db.Model):
    __tablename__ = "patients"

    ssn = db.Column(db.String(13), primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    date_of_birth = db.Column(db.DateTime(timezone=True), nullable=False)
    municipality = db.Column(db.Text, nullable=False)

    journal_entries = db.relationship(
        "JournalEntry",
        backref="patient",
        lazy=True
    )

    def __init__(self, ssn, firstname, surname, date_of_birth, municipality):
        self.ssn = ssn
        self.firstname = firstname
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.municipality = municipality

    def to_dict(self):
        return {
            "ssn": self.ssn,
            "date_of_birth": self.date_of_birth,
            "firstname": self.firstname,
            "surname": self.surname,
            "municipality": self.municipality,
        }

    @staticmethod
    def from_ssn(ssn):
        return Patient.query.filter_by(ssn=ssn).first()
