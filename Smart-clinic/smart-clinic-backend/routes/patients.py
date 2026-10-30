from flask import Blueprint, jsonify
from db import get_db_connection

patients_bp = Blueprint("patients", __name__)

@patients_bp.get("/")
def get_all_patients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patient")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)
