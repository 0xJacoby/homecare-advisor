from typing import Generator, List

from app import config
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
        return Categories.query.all()

    @staticmethod
    def all_from_ssn(
        ssn: str, 
        missing_categories_err = lambda category_name: category_name, 
    ) -> Generator[Category, None, None]:
        pi = PersonInfo(ssn)
        data = (
            db.session.query(JournalEntry, Categories)
            .filter_by(patient_ssn=ssn)
            .filter_by(test_id=1)
            .join(Categories, Categories.id == JournalEntry.test_value, isouter=True)
            .all()
        )

        for _, c in data:
            if c and config.category_index(c.name):
                yield Category.from_name(c.name, pi)
            elif c:
                missing_categories_err(c.name)


    @staticmethod
    def del_from_name(name: str):
        category = Categories.query.filter_by(name=name).first()
        if not category:
            return False

        db.session.delete(category)
        db.session.commit()
        return True
