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

    console.log("DATE CHANGED!");

    const doctorId = document.getElementById("doctor-select").value; // staff_id
    const date = document.getElementById("appointment-date").value;

    console.log("Doctor ID:", doctorId);
    console.log("Date value:", date);
    

    // Debug log to confirm values being sent
    console.log("📅 Fetching availability for staff_id:", doctorId, "date:", date);

    // If doctor or date is not selected, do nothing
    if (!doctorId || !date) {
        console.log("⚠️ Doctor or date not selected yet.");
        return;
    }

    try {
        // -------------------------------------------------------------
        // Call backend API to get available slots
        // NOTE: backend expects staff_id, NOT doctor_id
        // -------------------------------------------------------------
        const response = await fetch(
            `http://127.0.0.1:5000/appointments/availability?staff_id=${doctorId}&date=${date}`
        );

        console.log("📡 Availability API response status:", response.status);

        const data = await response.json();
        console.log("📦 Availability data received:", data);

        // Get the time slots container
        const slotContainer = document.getElementById("time-slots");
        slotContainer.innerHTML = ""; // clear old buttons

        // If no slots available
        if (!data.available_slots || data.available_slots.length === 0) {
            console.log("⛔ No available slots returned from backend.");
            slotContainer.innerHTML = "<p>No available slots for this date for your requested professional. Please select another date or different professional.</p>";
            return;
        }

        // -------------------------------------------------------------
        // Create a button for each available slot
        // -------------------------------------------------------------
        data.available_slots.forEach(slot => {
            const btn = document.createElement("button");
            btn.textContent = slot;
            btn.classList.add("slot");

            // When user clicks a slot, store it and highlight it
            btn.addEventListener("click", () => {
                selectedSlot = slot;
                console.log("⏰ Selected slot:", selectedSlot);

                // Remove highlight from all buttons
                document.querySelectorAll(".slot").forEach(b => b.classList.remove("selected"));

                // Highlight selected button
                btn.classList.add("selected");
            });

            slotContainer.appendChild(btn);
        });

        console.log("✅ Time slots displayed successfully.");

    } catch (error) {
        console.error("❌ Error fetching availability:", error);
    }
});

// -------------------------------------------------------------
// Confirm Appointment - Send booking request to backend
// -------------------------------------------------------------
document.getElementById("confirm-btn").addEventListener("click", async () => {

    const doctorId = document.getElementById("doctor-select").value; // staff_id
    const healthIssue = document.getElementById("health-issue").value;
    const reason = document.getElementById("reason").value;
    const date = document.getElementById("appointment-date").value;

    console.log("📝 Preparing booking...");
    console.log("Selected slot:", selectedSlot);

    // Check if a slot is selected
    if (!selectedSlot) {
        alert("Please select a time slot.");
        console.log("⚠️ Booking cancelled — no slot selected.");
        return;
    }

    // -------------------------------------------------------------
    // Prepare data to send to backend
    // NOTE: keys MUST match backend (staff_id, slot_time)
    // -------------------------------------------------------------
    const payload = {
        patient_id: patient.patient_id,
        staff_id: doctorId,
        date: date,
        slot_time: selectedSlot,
        health_issue: healthIssue,
        reason: reason
    };

    console.log("📤 Sending booking payload:", payload);

    try {
        // -------------------------------------------------------------
        // Send booking request to backend
        // -------------------------------------------------------------
        const response = await fetch("http://127.0.0.1:5000/appointments/book", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        console.log("📡 Booking API response status:", response.status);

        const result = await response.json();
        console.log("📦 Booking response:", result);

        // -------------------------------------------------------------
        // Show confirmation message
        // -------------------------------------------------------------
        if (result.error) {
            alert(result.error);
            console.log("❌ Booking failed:", result.error);
        } else {
            alert(result.message);
            console.log("✅ Booking successful!");

            // Reload availability so the booked slot disappears
            document.getElementById("appointment-date").dispatchEvent(new Event("change"));
        }

    } catch (error) {
        console.error("❌ Error booking appointment:", error);
        alert("Something went wrong while booking the appointment.");
    }
});
