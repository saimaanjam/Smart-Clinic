from flask import Blueprint, request, jsonify
from db import get_db_connection
import hashlib

login_bp = Blueprint("login", __name__)

@login_bp.post("/patient")
def patient_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Hash the incoming password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM patient WHERE email=%s AND password_hash=%s",
        (email, hashed_password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({"message": "Login successful", "user": user})
    else:
        return jsonify({"message": "Invalid credentials"}), 401
