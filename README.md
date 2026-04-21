# MongoDB Notes Sharing API

A simple Flask-based API to create and share notes between users using MongoDB.

## Logic Overview

- **User System**: Very basic user registration using a username.
- **Notes Storage**: 
    - Each note has an `owner_id`.
    - Each note has a `shared_with` list containing IDs of users who can see the note.
- **Sharing**: The owner of a note can add another user's ID to the `shared_with` list.
- **Retrieval**: When fetching notes for a user, the API returns both their owned notes and notes where their ID is in the `shared_with` list.

## Endpoints

1. **POST `/register`**
   - Body: `{"username": "string"}`
   - Registration of a new user.

2. **POST `/notes`**
   - Body: `{"user_id": "string", "content": "string", "title": "string"}`
   - Create a new note.

3. **GET `/notes/<user_id>`**
   - Returns personal and shared notes for the user.

4. **POST `/notes/<note_id>/share`**
   - Body: `{"owner_id": "string", "target_user_id": "string"}`
   - Share a note with another user.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure MongoDB is running on `localhost:27017`.
3. Run the app:
   ```bash
   python app.py
   ```
