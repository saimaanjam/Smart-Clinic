function setupSlotSelection() {

    document.querySelectorAll(".slot").forEach(slot => {

        slot.addEventListener("click", () => {

            document.querySelectorAll(".slot").forEach(btn => {
                btn.classList.remove("selected");
            });

            slot.classList.add("selected");

        });

    });

}