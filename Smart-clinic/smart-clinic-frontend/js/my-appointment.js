
// ---------------------------------------------------------
    // Retrieve the logged-in patient's information
    // from session storage.
    // The patient object is stored after successful login.
    // ---------------------------------------------------------
    const patientData = JSON.parse(sessionStorage.getItem("patient"));

    // ---------------------------------------------------------
    // Load appointments belonging to the logged-in patient
    // ---------------------------------------------------------
    async function loadAppointments() {

        // Get reference to the appointments container
        const container = document.getElementById("appointments-container");

        try {

            // ---------------------------------------------------------
            // Send request to Flask backend
            // The patient_id is used to retrieve only
            // this patient's appointments from the database.
            // ---------------------------------------------------------
            const response = await fetch(
                `http://127.0.0.1:5000/appointments/patient/${patientData.patient_id}`
            );

            // Convert response into JSON
            const appointments = await response.json();

            console.log("Appointments:",appointments);
            // ---------------------------------------------------------
            // If no appointments have been booked,
            // display a friendly message.
            // ---------------------------------------------------------
            if (appointments.length === 0) {

                container.innerHTML = `
                    <p>No appointments booked yet.</p>
                `;

                return;
            }

            // ---------------------------------------------------------
            // Generate appointment cards dynamically
            // using data returned from the database.
            // ---------------------------------------------------------
            container.innerHTML = appointments.map(appt => `

                <div class="appointment-card">

                    <h3>${appt.reason || "Consultation"}</h3>

                    
                    <p>
                        <strong>Date:</strong>
                        ${appt.slot_date}
                    </p>

                    <p>
                        <strong>Time:</strong>
                        ${appt.slot_time}
                    </p>

                    <p>
                        <strong>Clinician:</strong>
                        ${appt.first_name} ${appt.last_name}
                    </p>

                    <p>
                        <strong>Role:</strong>
                        ${appt.staff_role}
                    </p>

                    <p>
                        <strong>Health Issue:</strong>
                        ${appt.health_issue || "N/A"}
                    </p>

                    <p>
                        <strong>Status:</strong>
                        ${appt.slot_status}
                    </p>

                    <button
                    class="cancel-btn"
                    onclick="cancelAppointment(${appt.slots_id})">
                    Cancel Appointment
                    </button>

                </div>

            `).join("");

        } catch (error) {

            // ---------------------------------------------------------
            // If anything goes wrong (server unavailable,
            // network issue, route missing, etc.)
            // show an error message.
            // ---------------------------------------------------------
            console.error("Error loading appointments:", error);

            container.innerHTML = `
                <p>Unable to load appointments.</p>
            `;
        }
    }
    
        // ---------------------------------------------------------
// Cancel Appointment
// ---------------------------------------------------------
async function cancelAppointment(slotsId) {

    if (!confirm("Are you sure you want to cancel this appointment?")) {
        return;
    }

    try {

        const response = await fetch(
            `http://127.0.0.1:5000/appointments/cancel/${slotsId}`,
            {
                method: "PUT"
            }
        );

        const data = await response.json();

        alert(data.message);

        // Refresh appointment list
        loadAppointments();

    } catch (error) {

        console.error("Error cancelling appointment:", error);

        alert("Unable to cancel appointment.");

    }
}


    // ---------------------------------------------------------
    // Automatically load appointments when
    // the page opens.
    // ---------------------------------------------------------
    loadAppointments();

