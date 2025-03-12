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

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Document Loaded - Event Listeners Ready");

    /* Add Schedule Button */
    document.addEventListener("click", (e) => {
        if (e.target.classList.contains("schedule-btn")) {
            e.preventDefault(); // Prevent full-page reload
            toggleSchedulePopup();
            loadScheduleForm();
        }
    });

    // Ensure the "Save" button submits the form correctly
    document.addEventListener("click", async function (e) {
        if (e.target.id === "saveScheduleButton") {
            e.preventDefault(); // Stop default form submission

            const scheduleForm = document.getElementById("scheduleForm");
            if (!scheduleForm) {
                console.error("❌ Error: Schedule form not found!");
                return;
            }

            let formData = new FormData(scheduleForm);

            try {
                let response = await fetch("/schedule_medication", {
                    method: "POST",
                    body: formData
                });

                let result = await response.json();

                if (result.success) {
                    // Show success message inside the popup instead of printing JSON
                    const popupContent = document.querySelector(".schedule-popup-content");
                    popupContent.innerHTML = `<p style="color: green; font-weight: bold;">✅ Medication scheduled successfully!</p>`;

                    setTimeout(() => {
                        toggleSchedulePopup(); // Close the popup after 2 seconds
                        window.location.reload(); // Refresh the page to show the updated schedule
                    }, 2000);
                } else {
                    alert(`❌ Error: ${result.message}`);
                }
            } catch (error) {
                console.error("❌ Error submitting schedule:", error);
                alert("❌ An unexpected error occurred. Please try again.");
            }
        }
    });
});

/* Function to toggle schedule popup */
function toggleSchedulePopup() {
    console.log("✅ Toggling Schedule Popup...");
    const popup = document.querySelector(".schedule-popup");
    if (popup) {
        popup.classList.toggle("open");
        document.body.classList.toggle("hide-scrolling");
    } else {
        console.error("❌ Error: .schedule-popup element not found!");
    }
}

/* Function to dynamically load the schedule form */
function loadScheduleForm() {
    fetch("/schedule-med")
        .then(response => response.text())
        .then(html => {
            const popupContent = document.querySelector(".schedule-popup-content");
            if (!popupContent) {
                console.error("❌ Error: .schedule-popup-content not found!");
                return;
            }
            popupContent.innerHTML = html;

            console.log("✅ Schedule form loaded!");

            // Fetch medications for the selected patient
            fetchMedicationsForSelectedPatient();

            // Ensure tabs work inside the popup
            setTimeout(() => {
                loadScheduleTabs();
            }, 100);

            // Attach event listener for the cancel button inside the popup
            setTimeout(() => {
                const cancelButton = document.getElementById("cancelScheduleButton");
                if (cancelButton) {
                    cancelButton.addEventListener("click", (e) => {
                        e.preventDefault();
                        toggleSchedulePopup();
                    });
                    console.log("✅ Cancel button found and event added!");
                } else {
                    console.error("❌ Error: cancelScheduleButton not found!");
                }
            }, 300);
        })
        .catch(error => console.error("❌ Error loading the schedule form:", error));
}

/* Fetch Medications for Selected Patient */
function fetchMedicationsForSelectedPatient() {
    const selectedPatientId = sessionStorage.getItem("selectedPatientId"); // Get stored patient ID

    if (!selectedPatientId) {
        console.error("❌ No patient ID found in sessionStorage!");
        return;
    }

    console.log("📡 Fetching medications for patient ID:", selectedPatientId);

    fetch(`/get_medications/${selectedPatientId}`)
        .then(response => response.json())
        .then(data => {
            const medicationDropdown = document.getElementById("medication");
            if (!medicationDropdown) {
                console.error("❌ Error: Medication dropdown not found!");
                return;
            }

            // Clear existing options
            medicationDropdown.innerHTML = "";

            if (data.length === 0) {
                console.warn("⚠️ No medications found for this patient.");
                medicationDropdown.classList.add("placeholder"); // Apply placeholder styling
                medicationDropdown.setAttribute("disabled", "true"); // Disable if no medications
            } else {
                medicationDropdown.classList.remove("placeholder");
                medicationDropdown.removeAttribute("disabled");

                data.forEach(med => {
                    let option = document.createElement("option");
                    option.value = med.med_id;
                    option.textContent = med.med_name;
                    medicationDropdown.appendChild(option);
                });
            }

            console.log("✅ Medications loaded into dropdown:", data);
        })
        .catch(error => console.error("❌ Error fetching medications:", error));
}

/* Function to Handle Tabs Inside the Schedule Popup */
function loadScheduleTabs() {
    console.log("✅ Initializing Schedule Popup Tabs...");

    // Select all tab buttons inside the popup
    const tabButtons = document.querySelectorAll(".schedule-popup .tablinks");
    const tabContents = document.querySelectorAll(".schedule-popup .tabcontent");

    if (!tabButtons.length || !tabContents.length) {
        console.error("❌ Error: No tab buttons or contents found in popup!");
        return;
    }

    // Function to open a tab inside the popup
    function openScheduleTab(event, tabType) {
        console.log("🟢 Tab Clicked:", tabType);

        // Hide all tab contents
        tabContents.forEach(tab => tab.style.display = "none");

        // Remove active class from all tab buttons
        tabButtons.forEach(tab => tab.classList.remove("active"));

        // Show the clicked tab's content
        document.getElementById(tabType).style.display = "block";

        // Add active class to the clicked tab button
        event.currentTarget.classList.add("active");
    }

    // Attach event listeners to each tab button inside the popup
    tabButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            let tabType = event.target.getAttribute("data-type");
            openScheduleTab(event, tabType);
        });
    });

    // Ensure the first tab is selected when the popup opens
    setTimeout(() => {
        tabButtons[0].click();
    }, 200);
}
