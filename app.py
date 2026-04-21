from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/notes_sharing_api"
mongo = PyMongo(app)

# Helper to serialize MongoDB objects
def serialize_doc(doc):
    if doc:
        doc["_id"] = str(doc["_id"])
    return doc

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username required"}), 400
    
    if mongo.db.users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400
    
    user_id = mongo.db.users.insert_one({"username": username}).inserted_id
    return jsonify({"message": "User registered", "user_id": str(user_id)}), 201

@app.route("/notes", methods=["POST"])
def create_note():
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")
    title = data.get("title", "Untitled")

    if not user_id or not content:
        return jsonify({"error": "user_id and content required"}), 400

    note = {
        "owner_id": user_id,
        "title": title,
        "content": content,
        "shared_with": [],
        "created_at": datetime.datetime.utcnow()
    }
    note_id = mongo.db.notes.insert_one(note).inserted_id
    return jsonify({"message": "Note created", "note_id": str(note_id)}), 201

@app.route("/notes/<user_id>", methods=["GET"])
def get_notes(user_id):
    # Own notes
    own_notes = list(mongo.db.notes.find({"owner_id": user_id}))
    # Shared notes
    shared_notes = list(mongo.db.notes.find({"shared_with": user_id}))
    
    return jsonify({
        "own_notes": [serialize_doc(n) for n in own_notes],
        "shared_notes": [serialize_doc(n) for n in shared_notes]
    }), 200

@app.route("/notes/<note_id>/share", methods=["POST"])
def share_note(note_id):
    data = request.json
    owner_id = data.get("owner_id")
    target_user_id = data.get("target_user_id")

    if not owner_id or not target_user_id:
        return jsonify({"error": "owner_id and target_user_id required"}), 400

    note = mongo.db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        return jsonify({"error": "Note not found"}), 404
    
    if note["owner_id"] != owner_id:
        return jsonify({"error": "Unauthorized"}), 403

    if target_user_id in note["shared_with"]:
        return jsonify({"message": "Already shared"}), 200

    mongo.db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$push": {"shared_with": target_user_id}}
    )
    return jsonify({"message": f"Note shared with {target_user_id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
