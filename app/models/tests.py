from .. import db
from typing import Any, Dict, List, Optional, Tuple


class Tests(db.Model):
    __tablename__ = "tests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def id_from_name(name: str) -> Optional[int]:
        test = Tests.query.filter_by(name=name).first()

        if test:
            return test.id
        else:
            return None

    @staticmethod
    def get_all():
        return Tests.query.all()
