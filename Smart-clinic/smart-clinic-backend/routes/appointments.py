# ---------------------------------------------------------
# Appointments Blueprint
# ---------------------------------------------------------
# This file handles all appointment-related API routes.
# It includes:
#   - Getting all appointments
#   - Generating 15-minute time slots
#   - Checking available slots for a staff member on a date
#   - Generating 8 weeks of staff availability (doctors, nurses, midwives)
# ---------------------------------------------------------

from flask import Blueprint, request, jsonify
from db import get_db_connection
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

# Create a Blueprint for appointment routes
appointments_bp = Blueprint("appointments", __name__)
CORS(appointments_bp)

# ---------------------------------------------------------
# GET /appointments/
# Returns all appointments stored in the database.
# ---------------------------------------------------------
@appointments_bp.get("/")
def get_all_appointments():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM appointment")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)


# ---------------------------------------------------------
# Generate 15-minute time slots
# ---------------------------------------------------------
# Each slot represents:
#   - 10 minutes consultation
#   - 5 minutes gap
#
# Example:
#   start = "09:00"
#   end   = "10:00"
#   Output = ["09:00", "09:15", "09:30", "09:45"]
# ---------------------------------------------------------
def generate_time_slots(start, end):
    slots = []

    # Convert "HH:MM" strings into datetime objects
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")

    # Add 15-minute slots until reaching end_time
    while current < end_time:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=15)

    return slots


# ---------------------------------------------------------
# GET /appointments/availability
# ---------------------------------------------------------
# Returns available time slots for a staff member (doctor/nurse/midwife)
# on a specific date.
#
# Steps:
#   1. Read staff_id and date from query parameters
#   2. Fetch staff availability for that date
#   3. Generate all possible 15-minute slots
#   4. Fetch booked slots from booked_slots table
#   5. Remove booked slots from the list
#   6. Return remaining available slots
# ---------------------------------------------------------
# ---------------------------------------------------------
# GET /appointments/availability
# ---------------------------------------------------------
# Returns available time slots for a staff member (doctor/nurse/midwife)
# on a specific date.
#
# This version ALSO returns:
#   - staff_name
#   - staff_role
#
# Steps:
#   1. Read staff_id and date from query parameters
#   2. Fetch staff availability + name + role (JOIN)
#   3. Generate all possible 15-minute slots
#   4. Fetch booked slots from booked_slots table
#   5. Remove booked slots
#   6. Return remaining available slots + staff info
# ---------------------------------------------------------
@appointments_bp.get("/availability")
def get_availability():
    # Read query parameters from URL
    staff_id = request.args.get("staff_id")
    date = request.args.get("date")

    # If missing values, return an error
    if not staff_id or not date:
        return jsonify({"error": "staff_id and date are required"}), 400

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------------------------------------------------
    # Step 1: Fetch availability + staff name + role
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT 
            sa.staff_id,
            cs.first_name,
            cs.last_name,
            cs.staff_role,
            sa.available_date,
            sa.start_time,
            sa.end_time
        FROM staff_availability sa
        JOIN clinical_staff cs ON sa.staff_id = cs.staff_id
        WHERE sa.staff_id = %s AND sa.available_date = %s
    """, (staff_id, date))

    availability = cursor.fetchall()

    # If no availability found → staff has a day off
    if not availability:
        return jsonify({
            "staff_id": staff_id,
            "staff_name": None,
            "staff_role": None,
            "available_date": date,
            "available_slots": []
        })

    # Build full name
    staff_name = f"{availability[0]['first_name']} {availability[0]['last_name']}"

    # Extract start/end time from the first row
    start = availability[0]["start_time"]
    end = availability[0]["end_time"]

    # ---------------------------------------------------------
    # Step 2: Generate all possible time slots
    # ---------------------------------------------------------
    all_slots = generate_time_slots(start, end)

    # ---------------------------------------------------------
    # Step 3: Fetch booked slots for this staff + date
    # ---------------------------------------------------------
    cursor.execute("""
        SELECT slot_time
        FROM booked_slots
        WHERE staff_id=%s AND slot_date=%s
    """, (staff_id, date))

    booked_slots = [row["slot_time"] for row in cursor.fetchall()]

    # ---------------------------------------------------------
    # Step 4: Remove booked slots from the full list
    # ---------------------------------------------------------
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    # Close DB connection
    cursor.close()
    conn.close()

    # ---------------------------------------------------------
    # Step 5: Return final JSON response
    # ---------------------------------------------------------

    return jsonify({
        "staff_id": availability[0]["staff_id"],
        "staff_name": staff_name,
        "staff_role": availability[0]["staff_role"],
        "available_date": availability[0]["available_date"],
        "available_slots": available_slots
    })


# ---------------------------------------------------------
# Unified Staff Availability Generator
# ---------------------------------------------------------
# This function automatically creates availability for:
#   - 5 Doctors (each gets 1 rotating day off per week)
#   - Nurses (weekly rotation, only one nurse works each week)
#   - Midwives (weekly rotation, only one midwife works each week)
#
# It generates availability for the next 8 weeks.
# All availability is stored in the staff_availability table.
# ---------------------------------------------------------

def generate_all_staff_availability():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------------------------------------------------
    # 1. Fetch all staff from the database
    # ---------------------------------------------------------
    cursor.execute("SELECT staff_id, staff_role FROM clinical_staff")
    staff = cursor.fetchall()

    # Separate staff by role
    doctors = [s["staff_id"] for s in staff if s["staff_role"] == "Doctor"]
    nurses = [s["staff_id"] for s in staff if s["staff_role"] == "Nurse"]
    midwives = [s["staff_id"] for s in staff if s["staff_role"] == "Midwife"]

    # ---------------------------------------------------------
    # 2. Doctor scheduling rules
    # ---------------------------------------------------------
    # We expect exactly 5 doctors for the rotating day-off system.
    if len(doctors) != 5:
        return "Error: Rotation requires exactly 5 doctors."

    # Weekday names for rotation logic
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Doctor shift (same for all doctors)
    doctor_start = "09:00"
    doctor_end = "17:00"

    # ---------------------------------------------------------
    # 3. Nurse and Midwife weekly rotation rules
    # ---------------------------------------------------------
    nurse_start = "09:00"
    nurse_end = "17:00"

    midwife_start = "09:00"
    midwife_end = "17:00"

    # ---------------------------------------------------------
    # 4. Generate availability for the next 8 weeks
    # ---------------------------------------------------------
    start_date = datetime.now().date()
    end_date = start_date + timedelta(weeks=8)

    current_date = start_date

    while current_date <= end_date:
        weekday_index = current_date.weekday()  # Monday=0 ... Sunday=6

        # Only generate availability for Monday–Friday
        if weekday_index <= 4:

            # Determine which week number we are in
            week_number = ((current_date - start_date).days // 7)

            # ---------------------------------------------------------
            # DOCTORS: rotating day off
            # ---------------------------------------------------------
            for i, doctor_id in enumerate(doctors):
                # Calculate which day this doctor has off this week
                doctor_day_off = weekdays[(i + week_number) % 5]

                # If today is NOT their day off → generate availability
                if weekdays[weekday_index] != doctor_day_off:
                    cursor.execute("""
                        INSERT IGNORE INTO staff_availability (staff_id, available_date, start_time, end_time)
                        VALUES (%s, %s, %s, %s)
                    """, (doctor_id, current_date, doctor_start, doctor_end))

            # ---------------------------------------------------------
            # NURSES: weekly rotation (one nurse works the whole week)
            # ---------------------------------------------------------
            if nurses:
                nurse_index = week_number % len(nurses)
                nurse_id = nurses[nurse_index]

                cursor.execute("""
                    INSERT IGNORE INTO staff_availability (staff_id, available_date, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                """, (nurse_id, current_date, nurse_start, nurse_end))

            # ---------------------------------------------------------
            # MIDWIVES: weekly rotation (one midwife works the whole week)
            # ---------------------------------------------------------
            if midwives:
                midwife_index = week_number % len(midwives)
                midwife_id = midwives[midwife_index]

                cursor.execute("""
                    INSERT IGNORE INTO staff_availability (staff_id, available_date, start_time, end_time)
                    VALUES (%s, %s, %s, %s)
                """, (midwife_id, current_date, midwife_start, midwife_end))

        # Move to the next day
        current_date += timedelta(days=1)

    # Save all changes
    conn.commit()
    cursor.close()
    conn.close()

    return "Availability generated for all staff."

from flask_cors import cross_origin

# ---------------------------------------------------------
# Book an appointment slot for a staff member
# ---------------------------------------------------------
@appointments_bp.post("/book")
@cross_origin()
def book_slot():
    # Read JSON data sent from the frontend
    data = request.json

    # Extract required fields from the request body
    staff_id = data.get("staff_id")
    date = data.get("date")
    slot_time = data.get("slot_time")
    patient_id = data.get("patient_id")

    # Optional fields (extra information about the appointment)
    health_issue = data.get("health_issue")
    reason = data.get("reason")

    # ---------------------------------------------------------
    # Step 1: Validate required fields
    # ---------------------------------------------------------
    # If any of these are missing, the booking cannot be created
    if not staff_id or not date or not slot_time or not patient_id:
        return jsonify({"error": "Missing required fields"}), 400

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # ---------------------------------------------------------
    # Step 2: Check if the slot is already booked
    # ---------------------------------------------------------
    # Prevents double-booking the same staff/date/time
    cursor.execute("""
        SELECT * FROM booked_slots
        WHERE staff_id=%s AND slot_date=%s AND slot_time=%s
    """, (staff_id, date, slot_time))

    existing = cursor.fetchone()

    # If a record exists → slot is already taken
    if existing:
        cursor.close()
        conn.close()
        return jsonify({"error": "Slot already booked"}), 409

    # ---------------------------------------------------------
    # Step 3: Insert the new booking into the database
    # ---------------------------------------------------------
    cursor.execute("""
        INSERT INTO booked_slots (staff_id, patient_id, slot_date, slot_time, health_issue, reason, slot_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (staff_id, patient_id, date, slot_time, health_issue, reason, "booked"))

    # Save changes
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    # ---------------------------------------------------------
    # Step 4: Return success response
    # ---------------------------------------------------------
    return jsonify({
        "message": "Appointment booked successfully",
        "staff_id": staff_id,
        "patient_id": patient_id,
        "date": date,
        "slot_time": slot_time
    })

# ---------------------------------------------------------
# Temporary Test Route
# ---------------------------------------------------------
# This route allows you to trigger the availability generator
# from your browser:
#
#   GET /appointments/generate_availability
#
# Useful for testing and development.
# ---------------------------------------------------------
@appointments_bp.get("/generate_availability")
def generate_availability_route():
    result = generate_all_staff_availability()
    return jsonify({"message": result})

# ---------------------------------------------------------
# Get appointments for a specific patient
# ---------------------------------------------------------
from flask_cors import cross_origin

# ---------------------------------------------------------
# GET /appointments/patient/<patient_id>
#
# Returns all appointments booked by a specific patient.
#
# IMPORTANT:
# MySQL TIME values are returned as timedelta objects.
# Flask's jsonify() cannot convert timedelta objects into JSON,
# which causes:
#
# TypeError: Object of type timedelta is not JSON serializable
#
# Before returning data to the frontend, convert slot_time
# into a string so it can be serialized correctly.
#
# Also enable CORS for requests coming from the frontend
# running on http://127.0.0.1:5500.
# ---------------------------------------------------------
@appointments_bp.get("/patient/<int:patient_id>")
@cross_origin(origins=["http://127.0.0.1:5500"])
def get_patient_appointments(patient_id):

    # Connect to database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Retrieve appointments for the logged-in patient
    cursor.execute("""
        SELECT
            bs.slots_id,
            bs.slot_date,
            bs.slot_time,
            bs.reason,
            bs.health_issue,
            bs.slot_status,
            cs.first_name,
            cs.last_name,
            cs.staff_role
        FROM booked_slots bs
        JOIN clinical_staff cs
            ON bs.staff_id = cs.staff_id
        WHERE bs.patient_id = %s
        ORDER BY bs.slot_date DESC
    """, (patient_id,))

    appointments = cursor.fetchall()

    # ---------------------------------------------------------
    # FIX:
    # Convert MySQL TIME (timedelta) into a string.
    #
    # Without this conversion Flask raises:
    # "Object of type timedelta is not JSON serializable"
    # ---------------------------------------------------------
    for appt in appointments:
        if appt["slot_time"]:
            appt["slot_time"] = str(appt["slot_time"])

    # Close database connection
    cursor.close()
    conn.close()

    # Return appointment data as JSON
    return jsonify(appointments), 200

# ---------------------------------------------------------
# PUT /appointments/cancel/<slots_id>
#
# Cancels an existing appointment by updating the
# slot_status field in the booked_slots table.
#
# Example:
#   Before cancellation:
#       slot_status = "booked"
#
#   After cancellation:
#       slot_status = "cancelled"
#
# This approach is preferred because it keeps a
# record of the appointment instead of deleting it
# from the database.
# ---------------------------------------------------------
@appointments_bp.put("/cancel/<int:slots_id>")
@cross_origin(origins=["http://127.0.0.1:5500"])
def cancel_appointment(slots_id):

    # ---------------------------------------------------------
    # Connect to the database
    # ---------------------------------------------------------
    conn = get_db_connection()
    cursor = conn.cursor()

    # ---------------------------------------------------------
    # Update the appointment status
    #
    # Find the appointment using its primary key (slots_id)
    # and change the current status to "cancelled".
    # ---------------------------------------------------------
    cursor.execute("""
        UPDATE booked_slots
        SET slot_status = 'cancelled'
        WHERE slots_id = %s
    """, (slots_id,))

    # ---------------------------------------------------------
    # Save changes to the database
    # ---------------------------------------------------------
    conn.commit()

    # ---------------------------------------------------------
    # Close database resources
    # ---------------------------------------------------------
    cursor.close()
    conn.close()

    # ---------------------------------------------------------
    # Return success message to frontend
    # ---------------------------------------------------------
    return jsonify({
        "message": "Appointment cancelled successfully."
    })



