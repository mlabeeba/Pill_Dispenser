function saveChanges() {
    const data = [];
    const rows = document.querySelectorAll('#medications-table-body tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('.editable');
        const row_data = {
            med_id: row.cells[0].textContent, // assuming the ID is stored in the first cell
            med_name: cells[0].textContent,
            dosage: cells[1].textContent,
            stock_levels: cells[2].textContent,
            med_notes: cells[3].textContent
        };
        data.push(row_data);
    });

    // Send data to server with fetch
    fetch('/update_medications', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log('Success:', result);
        if(result.success) {
            alert('Updates saved successfully!');
        } else {
            alert('Failed to save updates.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error saving updates.');
    });
}
