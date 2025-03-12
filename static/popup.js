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
        e.preventDefault(); // Stop any form submission or link navigation
        toggleSchedulePopup(); // Open the popup
        loadScheduleForm(); // Load the schedule form dynamically
    }
});

// Function to toggle the schedule popup visibility
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

// Function to dynamically load the schedule form
function loadScheduleForm() {
    fetch('/schedule-med')
        .then(response => response.text())
        .then(html => {
            const popupContent = document.querySelector(".schedule-popup-content");
            if (!popupContent) {
                console.error("❌ Error: .schedule-popup-content not found!");
                return;
            }
            popupContent.innerHTML = html;

            console.log("✅ Schedule form loaded!"); // Debugging

            // Ensure tabs work inside the popup
            setTimeout(() => {
                loadScheduleTabs();
            }, 100); // Ensure DOM updates before running

            // Ensure the cancel button exists before adding event listener
            setTimeout(() => {
                const cancelButton = document.getElementById("cancelScheduleButton");
                if (cancelButton) {
                    cancelButton.addEventListener("click", (e) => {
                        e.preventDefault(); // Prevent default behavior
                        toggleSchedulePopup(); // Close popup without validation
                    });
                    console.log("✅ Cancel button found and event added!");
                } else {
                    console.error("❌ Error: cancelScheduleButton not found! Check schedule-med.html.");
                }
            }, 300);

            // Ensure the form only submits when clicking "Save"
            const scheduleForm = document.getElementById("scheduleForm");
            if (scheduleForm) {
                document.getElementById("saveScheduleButton").addEventListener("click", (e) => {
                    e.preventDefault(); // Stop form from submitting on its own

                    // Get selected tab
                    const activeTab = document.querySelector(".tablinks.active").getAttribute("data-type");

                    let valid = true;
                    let data = {};

                    if (activeTab === "time") {
                        data.scheduleDate = document.getElementById("scheduleDate").value;
                        data.scheduleTime = document.getElementById("scheduleTime").value;
                        if (!data.scheduleDate || !data.scheduleTime) {
                            valid = false;
                        }
                    } else if (activeTab === "interval") {
                        data.intervalDays = document.getElementById("intervalDays").value;
                        data.intervalHours = document.getElementById("intervalHours").value;
                        if (!data.intervalDays || !data.intervalHours) {
                            valid = false;
                        }
                    }

                    if (!valid) {
                        alert("⚠️ Please fill in all fields before submitting.");
                        return;
                    }

                    console.log("✅ Form submitted:", data);

                    // Show success message & close the popup
                    alert("✅ Medication scheduled successfully!");
                    toggleSchedulePopup();
                });
            } else {
                console.error("❌ Error: scheduleForm not found!");
            }
        })
        .catch(error => console.error("❌ Error loading the schedule form:", error));
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
