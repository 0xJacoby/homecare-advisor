from app import db, Application

app = Application()

with app.db.app_context():
    db.create_all()

if __name__ == "__main__":
    app.db.run(debug=True)
