# Productivity App API

## Description

Productivity App API is a RESTful backend application built with Python and Flask. It allows users to register, log in, manage their sessions and perform CRUD operations on their personal notes.

The API uses session-based authentication to protect private routes and ensures that users can only access and manage their own notes.

## Technologies Used

- Python 3.12
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite
- Pipenv

## Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd full-auth-productivity-app
```

### 2. Install dependencies

```bash
pipenv install --dev
```

### 3. Set the secret key

For local development, set an environment variable:

```bash
export SECRET_KEY="your-own-secret-key"
```

### 4. Apply database migrations

```bash
FLASK_APP=app.py pipenv run flask db upgrade
```

### 5. Seed the database

```bash
pipenv run python seed.py
```

### 6. Start the application

```bash
pipenv run python app.py
```

The API runs at:

`http://127.0.0.1:5555`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/signup` | Register a new user |
| POST | `/login` | Log in a user |
| DELETE | `/logout` | Log out the current user |
| GET | `/check_session` | Check the current session |
| GET | `/me` | Retrieve the current logged-in user |

### Notes

All notes endpoints require an authenticated session.

| Method | Endpoint | Description |
|---|---|---|
| GET | `/notes` | Retrieve the logged-in user's notes |
| POST | `/notes` | Create a new note |
| PATCH | `/notes/<note_id>` | Update an existing note |
| DELETE | `/notes/<note_id>` | Delete a note |

## Pagination

The notes endpoint supports pagination through query parameters.

Example:

```text
GET /notes?page=1&per_page=10
```

- `page`: The page number.
- `per_page`: The number of notes returned per page.

The API returns the notes together with pagination information, including the total number of notes and pages.

## Authentication and Security

- Passwords are hashed using Flask-Bcrypt.
- Authentication is managed using Flask sessions.
- Protected endpoints require an authenticated session.
- Users can only access, update and delete their own notes.
- Password hashes are never included in user responses.

Postman can be used to test the API. Keep cookies enabled so that the session is maintained between requests.

## Seed Data

Run `seed.py` to create example users and notes.

The development seed users are:

| Username | Password |
|---|---|
| ralph | password123 |
| john | password123 |

These credentials are for development and testing only.

## Project Structure

```text
full-auth-productivity-app/
│
├── app.py
├── extensions.py
├── models.py
├── seed.py
├── migrations/
├── instance/
├── Pipfile
├── Pipfile.lock
├── README.md
└── .gitignore
```

## Author

Ralph Njuguna