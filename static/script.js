// Function to handle the form submission for adding a new record
function addRecord(event) {
  event.preventDefault(); // Prevent the form from submitting normally
  // Get the form inputs
  const nameInput = document.getElementById('name');
  const emailInput = document.getElementById('email');
  // Create an object with the form data
  const formData = {
    name: nameInput.value,
    email: emailInput.value
  };
  // Send a POST request to the backend to add the record
  fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
//    ,
//    body: JSON.stringify(formData)
  })
//  .then(response => response.json())
//  .then(data => {
//    // Handle the response from the backend
//    console.log(data); // You can customize this based on your requirements
//
//    // Clear the form inputs
//    nameInput.value = '';
//    emailInput.value = '';
//
//    // Refresh the records table
//    fetchRecords();
//  })
  .catch(error => {
    console.error('Error:', error);
  });
}

// Function to handle the click event for deleting a record
function deleteRecord(recordId) {
  // Send a DELETE request to the backend to delete the record
  fetch(`/delete/${recordId}`, {
    method: 'POST'
  })
  .then(response => response.text)

  .then(data => {
    // Handle the response from the backend
    console.log(data); // You can customize this based on your requirements

    // Refresh the records table
    fetchRecords();
  })
  .catch(error => {
    console.error('Error:', error);
  });
//    console.log(response);
  location.reload();
}

// Function to fetch the records from the backend and update the table
function fetchRecords() {
  // Send a GET request to the backend to retrieve the records
  fetch('/record')
    .then(response => response.json())
    .then(records => {
      // Update the records table with the fetched data
      const tableBody = document.querySelector('#records-table tbody');
      tableBody.innerHTML = ''; // Clear the existing table rows

      records.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${record.FirstName}</td>
          <td>${record.LastName}</td>
          <td>${record.Email}</td>
          <td>${record.Phone}</td>
          <td>${record.City}</td>
          <td>
            <button onclick="editRecord(${record.ID})">Edit</button>
            <button onclick="deleteRecord(${record.ID})">Delete</button>
          </td>
        `;
        tableBody.appendChild(row);
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Function to handle the initial page load and fetch the records
document.addEventListener('DOMContentLoaded', () => {
  fetchRecords();
});
