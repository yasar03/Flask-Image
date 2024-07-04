// document.getElementById('upload-form').addEventListener('submit', function(e) {
//     e.preventDefault();
    
//     const fileInput = document.getElementById('csv-file');
//     const file = fileInput.files[0];
    
//     const formData = new FormData();
//     formData.append('file', file);
    
//     fetch('https://flask-image-koam.onrender.com/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data);
//         alert('File uploaded successfully');
//     })
//     .catch(error => console.error('Error:', error));
// });

// function queryData() {
//     const key = document.getElementById('filter-key').value;
//     const value = document.getElementById('filter-value').value;
    
//     if (key && value) {
//         fetch(`https://flask-image-koam.onrender.com/query?${key}=${value}`)
//         .then(response => response.json())
//         .then(data => {
//             const resultsDiv = document.getElementById('results');
//             resultsDiv.innerHTML = '';  // Clear previous results
            
//             if (data.length === 0) {
//                 resultsDiv.innerHTML = '<p>No results found.</p>';
//                 return;
//             }
            
//             const table = document.createElement('table');
//             table.classList.add('results-table');
            
//             // Create table headers
//             const headers = Object.keys(data[0]);
//             const headerRow = document.createElement('tr');
//             headers.forEach(header => {
//                 const th = document.createElement('th');
//                 th.textContent = header;
//                 headerRow.appendChild(th);
//             });
//             table.appendChild(headerRow);
            
//             // Populate table rows
//             data.forEach(item => {
//                 const row = document.createElement('tr');
//                 headers.forEach(header => {
//                     const td = document.createElement('td');
//                     td.textContent = item[header];
//                     row.appendChild(td);
//                 });
//                 table.appendChild(row);
//             });
            
//             resultsDiv.appendChild(table);
//         })
//         .catch(error => console.error('Error:', error));
//     } else {
//         alert('Please enter both filter key and value');
//     }
// }


document.getElementById('user-type').addEventListener('change', function() {
    const userType = document.getElementById('user-type').value;
    const adminPassword = document.getElementById('admin-password');
    if (userType === 'admin') {
        adminPassword.style.display = 'block';
    } else {
        adminPassword.style.display = 'none';
    }
});

document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const userType = document.getElementById('user-type').value;
    const password = document.getElementById('password').value;

    fetch('https://flask-image-koam.onrender.com/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_type: userType, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('login-container').style.display = 'none';
            document.getElementById('main-container').style.display = 'block';
            populateColumns();  // Fetch column names after successful login
            alert('Login successful');
        } else {
            alert('Login failed: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('csv-file');
    const file = fileInput.files[0];
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('https://flask-image-koam.onrender.com/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('File uploaded successfully');
        populateColumns();  // Fetch column names after uploading the file
    })
    .catch(error => console.error('Error:', error));
});

function queryData() {
    const key = document.getElementById('filter-key').value;
    const value = document.getElementById('filter-value').value;
    
    if (key && value) {
        fetch(`https://flask-image-koam.onrender.com/query?${key}=${value}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';  // Clear previous results
            
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No results found.</p>';
                return;
            }
            
            const table = document.createElement('table');
            table.classList.add('results-table');
            
            // Create table headers
            const headers = Object.keys(data[0]);
            const headerRow = document.createElement('tr');
            headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);
            
            // Populate table rows
            data.forEach(item => {
                const row = document.createElement('tr');
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.textContent = item[header];
                    row.appendChild(td);
                });
                table.appendChild(row);
            });
            
            resultsDiv.appendChild(table);
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter both filter key and value');
    }
}

function populateColumns() {
    fetch('https://flask-image-koam.onrender.com/columns')
    .then(response => response.json())
    .then(columns => {
        const filterKeySelect = document.getElementById('filter-key');
        filterKeySelect.innerHTML = '';  // Clear previous options
        columns.forEach(column => {
            const option = document.createElement('option');
            option.value = column;
            option.textContent = column;
            filterKeySelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error:', error));
}
