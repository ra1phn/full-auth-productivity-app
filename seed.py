from app import app
from extensions import db
from models import User, Note


with app.app_context():

    # Create the database tables if they do not exist
    db.create_all()

    # Create the first user
    user1 = User.query.filter_by(username="ralph").first()

    if user1 is None:
        user1 = User(username="ralph")
        user1.set_password("password123")
        db.session.add(user1)
        db.session.commit()

    # Create the second user
    user2 = User.query.filter_by(username="john").first()

    if user2 is None:
        user2 = User(username="john")
        user2.set_password("password123")
        db.session.add(user2)
        db.session.commit()

    # Create example notes for Ralph
    if not Note.query.filter_by(user_id=user1.id).first():
        note1 = Note(
            title="Complete Flask project",
            content="Finish authentication and CRUD routes.",
            user_id=user1.id
        )

        note2 = Note(
            title="Study Python",
            content="Practise Python and Flask every day.",
            user_id=user1.id
        )

        db.session.add_all([note1, note2])

    # Create an example note for John
    if not Note.query.filter_by(user_id=user2.id).first():
        note3 = Note(
            title="My personal goals",
            content="Organise my weekly tasks.",
            user_id=user2.id
        )

        db.session.add(note3)

    db.session.commit()

    print("Database seeded successfully!")
