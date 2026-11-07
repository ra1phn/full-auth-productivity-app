from flask import Flask, request, jsonify, session
from functools import wraps
import os

from extensions import db, migrate
from models import User, Note


app = Flask(__name__)

# Application configuration
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "development-secret-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///productivity.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialise extensions
db.init_app(app)
migrate.init_app(app, db)


# Protect routes that require a logged-in user
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401

        return func(*args, **kwargs)

    return wrapper


# -------------------------
# AUTHENTICATION ROUTES
# -------------------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    username = username.strip()

    if not username:
        return jsonify({"error": "Username cannot be empty"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    user = User(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username.strip()).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    session.clear()
    session["user_id"] = user.id

    return jsonify(user.to_dict()), 200


@app.route("/logout", methods=["DELETE"])
def logout():
    session.clear()

    return "", 204


@app.route("/check_session", methods=["GET"])
@app.route("/me", methods=["GET"])
@login_required
def check_session():
    user = db.session.get(User, session["user_id"])

    if user is None:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify(user.to_dict()), 200


# -------------------------
# NOTES ROUTES
# -------------------------

@app.route("/notes", methods=["GET"])
@login_required
def get_notes():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if page < 1 or per_page < 1:
        return jsonify({"error": "Invalid pagination values"}), 400

    # Limit the number of notes returned per request
    per_page = min(per_page, 100)

    user_id = session["user_id"]

    query = Note.query.filter_by(user_id=user_id)

    total_notes = query.count()

    notes = query.order_by(Note.id).offset(
        (page - 1) * per_page
    ).limit(per_page).all()

    return jsonify({
        "notes": [note.to_dict() for note in notes],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total_notes,
            "pages": (total_notes + per_page - 1) // per_page
        }
    }), 200


@app.route("/notes", methods=["POST"])
@login_required
def create_note():
    data = request.get_json(silent=True) or {}

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    note = Note(
        title=title,
        content=content,
        user_id=session["user_id"]
    )

    db.session.add(note)
    db.session.commit()

    return jsonify(note.to_dict()), 201


@app.route("/notes/<int:note_id>", methods=["PATCH"])
@login_required
def update_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if note is None:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json(silent=True) or {}

    if "title" in data:
        if not data["title"]:
            return jsonify({"error": "Title cannot be empty"}), 400
        note.title = data["title"]

    if "content" in data:
        if not data["content"]:
            return jsonify({"error": "Content cannot be empty"}), 400
        note.content = data["content"]

    db.session.commit()

    return jsonify(note.to_dict()), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(
        id=note_id,
        user_id=session["user_id"]
    ).first()

    if note is None:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    app.run(port=5555, debug=True)
