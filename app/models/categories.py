from .. import db
from app.models.journal_entry import JournalEntry
from app.person_info import PersonInfo
from app.category import Category


class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    @staticmethod
    def from_id(id):
        return Categories.query.get(id)

    @staticmethod
    def get_all():
        data = Categories.query.all()
        return [c.name for _, c in data]

    @staticmethod
    def all_from_ssn(ssn: int) -> [str]:
        pi = PersonInfo(ssn)
        data = (
            db.session.query(JournalEntry, Categories)
            .filter_by(ssn=ssn)
            .filter_by(test_id=1)
            .join(Categories, Categories.id == JournalEntry.test_value, isouter=True)
            .all()
        )

        return [Category.from_name(c.name, pi) for _, c in data]
