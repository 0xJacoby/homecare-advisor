from app.db import db


class Categories(db.Model):
    __tablename__ = 'categories'

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
