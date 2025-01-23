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
                event.preventDefault();
                toggleMedicationPopup();
                alert("Medication scheduled successfully!");
            });
        })
        .catch(error => console.error("Error loading the form:", error));
}
