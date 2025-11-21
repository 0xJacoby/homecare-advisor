from app import db, Application
from app.models import Tests

app = Application()

with app.db.app_context():
    db.create_all()

    if len(Tests.query.all()) == 0:
        categories_test = Tests("Categories")
        db.session.add(categories_test)
        db.session.commit()

if __name__ == "__main__":
    app.db.run(debug=True)
