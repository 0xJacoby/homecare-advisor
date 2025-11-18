from .. import db


class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.String(13), db.ForeignKey(
        "patients.ssn"), nullable=False)
    entry_date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, patient_ssn, entry_date, content):
        self.patient_ssn = patient_ssn
        self.entry_date = entry_date
        self.content = content

    def to_dict(self):
        return {
            "id": self.id,
            "patient_ssn": self.patient_ssn,
            "entry_date": self.entry_date,
            "content": self.content
        }

    @staticmethod
    def from_ssn(ssn):
        return JournalEntry.query.filter_by(patient_ssn=ssn).all()
