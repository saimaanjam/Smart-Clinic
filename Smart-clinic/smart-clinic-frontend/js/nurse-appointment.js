// -------------------------------------------------------------
// Load logged-in patient name from sessionStorage
// -------------------------------------------------------------
const patient = JSON.parse(sessionStorage.getItem("patient"));
if (patient) {
    document.getElementById("patient-name").textContent =
        `Welcome, ${patient.first_name} ${patient.last_name}`;
}

// -------------------------------------------------------------
// Variables
// -------------------------------------------------------------
let selectedSlot = null; // stores the time slot the user clicks

// -------------------------------------------------------------
// Fetch available time slots when the date changes
// -------------------------------------------------------------
document.getElementById("appointment-date").addEventListener("change", async () => {

    const nurseId = document.getElementById("nurse-select").value; // staff_id
    const date = document.getElementById("appointment-date").value;

    if (!nurseId || !date) return;

    try {
        const response = await fetch(
            `http://127.0.0.1:5000/appointments/availability?staff_id=${nurseId}&date=${date}`
        );

        const data = await response.json();

        const slotContainer = document.getElementById("time-slots");
        slotContainer.innerHTML = "";

        if (!data.available_slots || data.available_slots.length === 0) {
            slotContainer.innerHTML = "<p>No available slots for this date for your requested professional. Please select another date or different professional.</p>";
            return;
        }

        data.available_slots.forEach(slot => {
            const btn = document.createElement("button");
            btn.textContent = slot;
            btn.classList.add("slot");

            btn.addEventListener("click", () => {
                selectedSlot = slot;

                document.querySelectorAll(".slot")
                    .forEach(b => b.classList.remove("selected"));

                btn.classList.add("selected");
            });

            slotContainer.appendChild(btn);
        });

    } catch (error) {
        console.error("Error fetching availability:", error);
    }
});

// -------------------------------------------------------------
// Confirm Appointment - Send booking request to backend
// -------------------------------------------------------------
document.getElementById("confirm-btn").addEventListener("click", async () => {

    const nurseId = document.getElementById("nurse-select").value;
    const healthIssue = document.getElementById("health-issue").value;
    const reason = document.getElementById("reason").value;
    const date = document.getElementById("appointment-date").value;

    if (!selectedSlot) {
        alert("Please select a time slot.");
        return;
    }

    const payload = {
        patient_id: patient.patient_id,
        staff_id: nurseId,
        date: date,
        slot_time: selectedSlot,
        health_issue: healthIssue,
        reason: reason
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/appointments/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (result.error) {
            alert(result.error);
        } else {
            alert(result.message);

            // Reload availability so the booked slot disappears
            document.getElementById("appointment-date")
                .dispatchEvent(new Event("change"));
        }

    } catch (error) {
        console.error("Error booking appointment:", error);
        alert("Something went wrong while booking the appointment.");
    }
});
