async function fetchRecords(page = 1, size = 20) {

    const apiUrl = `/api/records?page=${page}&size=${size}`;
    const container = document.getElementById('data-container');
    container.innerHTML = '<p>Loading records...</p>';

    try {
        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        
        // The 'data' field is a JSON string -> repeat parse
        const records = JSON.parse(jsonResponse.data); 
        const metadata = jsonResponse.metadata;

        renderRecords(records, container);
        renderPagination(metadata);

    } catch (error) {
        console.error("Could not fetch records:", error);
        container.innerHTML = `<p style="color: red;">Error fetching data: ${error.message}. Please check the server logs.</p>`;
    }
}

function renderRecords(records, container) {
    if (records.length === 0) {
        container.innerHTML = '<p>No records found.</p>';
        return;
    }

    const table = document.createElement('table');
    table.classList.add('records-table'); // TODO: Add css later

    const headers = Object.keys(records[0]);

    const tableHeader = table.createTHead();
    const headerRow = tableHeader.insertRow();
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText.toUpperCase();
        headerRow.appendChild(th);
    });

    const tbody = table.createTBody();
    records.forEach(record => {
        const row = tbody.insertRow();
        headers.forEach(headerKey => {
            const cell = row.insertCell();
            cell.textContent = record[headerKey];
        });
    });

    // Clear the container and append the table
    container.innerHTML = '';
    container.appendChild(table);
}

function renderPagination(metadata) {
    const { page, total_pages } = metadata;
    let paginationHtml = '<div class="pagination-controls">';

    // Previous button
    if (page > 1) {
        paginationHtml += `<button onclick="fetchRecords(${page - 1}, ${metadata.size})">Previous</button>`;
    } else {
        paginationHtml += `<button disabled>Previous</button>`;
    }

    // Page info
    paginationHtml += `<span>Page ${page} of ${total_pages}</span>`;

    // Next button
    if (page < total_pages) {
        paginationHtml += `<button onclick="fetchRecords(${page + 1}, ${metadata.size})">Next</button>`;
    } else {
        paginationHtml += `<button disabled>Next</button>`;
    }
    
    paginationHtml += '</div>';

    // Append to a designated pagination area (you'd need to create this in your HTML)
    let paginationContainer = document.getElementById('pagination-area');
    if (!paginationContainer) {
        paginationContainer = document.createElement('div');
        paginationContainer.id = 'pagination-area';
        document.getElementById('data-container').after(paginationContainer); // Place after the data
    }

    paginationContainer.innerHTML = paginationHtml;
}

// Initial call to load the first page
document.addEventListener('DOMContentLoaded', () => {
    fetchRecords(1, 20);
});