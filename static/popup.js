/* Add Medication Button */
// ---------------------- /

// Add an event listener for the "Add" button
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("add-med-btn")) {
        toggleMedicationPopup(); // Open or close the popup
        loadMedicationForm(); // Dynamically load the form
    }
});

// Function to toggle the popup visibility
function toggleMedicationPopup() {
    document.querySelector(".medication-popup").classList.toggle("open");
    document.body.classList.toggle("hide-scrolling");
}

// Function to load the form dynamically
function loadMedicationForm() {
    fetch('/add-med')
        .then(response => response.text())
        .then(html => {
            const popupContent = document.querySelector(".medication-popup-content");
            popupContent.innerHTML = html;

            // Add event listener for the cancel button inside the popup
            const cancelButton = document.getElementById("cancelButton");
            cancelButton.addEventListener("click", toggleMedicationPopup);

            // Add event listener for the form submission
            const medicationForm = document.getElementById("medicationForm");
            medicationForm.addEventListener("submit", (event) => {
                //event.preventDefault();
                toggleMedicationPopup();
                alert("Medication scheduled successfully!");
            });
        })
        .catch(error => console.error("Error loading the form:", error));
}

/* Add Patient Button */
// ---------------------- /
document.addEventListener("DOMContentLoaded", function () {
    // Listener for the "Add Patient" button
    document.addEventListener("click", (e) => {
        if (e.target.classList.contains("add-patient-btn")) {
            togglePatientPopup(); // Open or close the popup
            loadPatientForm(); // Dynamically load the form
        }
    });

    // Function to toggle the patient popup visibility
    function togglePatientPopup() {
        const patientPopup = document.querySelector(".patient-popup");
        patientPopup.classList.toggle("open");
        document.body.classList.toggle("hide-scrolling");
    }

    // Function to dynamically load the patient form
    function loadPatientForm() {
        fetch('/add-patient')
            .then(response => response.text())
            .then(html => {
                const popupContent = document.querySelector(".patient-popup-content");
                popupContent.innerHTML = html;
                document.getElementById("cancelButton").addEventListener("click", togglePatientPopup);
            })
            .catch(error => console.error("Error loading the form:", error));
    }
});

/* Add Schedule Button */
// ---------------------- /
document.addEventListener("click", (e) => {
    if (e.target.classList.contains("schedule-btn")) {
        toggleSchedulePopup(); // Open or close the popup
        loadScheduleForm(); // Dynamically load the form
    }
});

// Function to toggle the schedule popup visibility
function toggleSchedulePopup() {
    document.querySelector(".schedule-popup").classList.toggle("open");
    document.body.classList.toggle("hide-scrolling");
}

// Function to dynamically load the schedule form
function loadScheduleForm() {
    fetch('/schedule-med')
        .then(response => response.text())
        .then(html => {
            const popupContent = document.querySelector(".schedule-popup-content");
            popupContent.innerHTML = html;

            // Add event listener for the cancel button inside the popup
            const cancelButton = document.getElementById("cancelScheduleButton");
            cancelButton.addEventListener("click", toggleSchedulePopup);

            // Add event listener for the form submission
            const scheduleForm = document.getElementById("scheduleForm");
            scheduleForm.addEventListener("submit", (event) => {
                event.preventDefault();
                toggleSchedulePopup();
                alert("Medication scheduled successfully!");
            });
        })
        .catch(error => console.error("Error loading the schedule form:", error));
}
