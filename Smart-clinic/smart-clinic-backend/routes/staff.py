from flask import Blueprint, jsonify
from db import get_db_connection

staff_bp = Blueprint("staff", __name__)

@staff_bp.get("/")
def get_all_staff():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clinical_staff")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)
