from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

from routes.patients import patients_bp
from routes.staff import staff_bp
from routes.appointments import appointments_bp
from routes.queue import queue_bp
from routes.login import login_bp

app.register_blueprint(patients_bp, url_prefix="/patients")
app.register_blueprint(staff_bp, url_prefix="/staff")
CORS(appointments_bp, resources={r"/*": {"origins": "*"}})
app.register_blueprint(appointments_bp, url_prefix="/appointments")
app.register_blueprint(queue_bp, url_prefix="/queue")
app.register_blueprint(login_bp, url_prefix="/auth")

if __name__ == "__main__":
    app.run(debug=True)
