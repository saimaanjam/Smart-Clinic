from flask import Blueprint, jsonify
from db import get_db_connection

queue_bp = Blueprint("queue", __name__)

@queue_bp.get("/")
def get_queue():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM queue")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)
