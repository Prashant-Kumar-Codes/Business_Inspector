/*
 * inspect.js
 * Handles file upload interactions, drag-and-drop, and the UI transition
 * from uploading -> processing -> results.
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const uploadForm = document.getElementById('upload-form');
    const dropZoneText = dropZone.querySelector('p');

    const uploadSection = document.getElementById('upload-section');
    const processingSection = document.getElementById('processing-section');
    const resultsSection = document.getElementById('results-section');

    // --- 1. Drag & Drop Handlers ---
    
    // Highlight drop zone on drag over
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    // Remove highlight when drag leaves
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    // Handle click to browse
    dropZone.addEventListener('click', (e) => {
        if (e.target !== fileInput) {
            fileInput.click();
        }
    });

    // Handle standard file input change
    fileInput.addEventListener('change', (e) => {
        if (fileInput.files.length > 0) {
            handleFileSelection(fileInput.files[0]);
        }
    });

    // --- 2. File Selection Logic ---
    function handleFileSelection(file) {
        // Validate file type
        const validExtensions = ['.csv', '.xlsx'];
        const fileName = file.name;
        const isValid = validExtensions.some(ext => fileName.toLowerCase().endsWith(ext));

        if (isValid) {
            // Update UI to show selected file
            dropZoneText.innerHTML = `Selected file: <strong>${fileName}</strong>`;
            uploadBtn.disabled = false; // Enable submit button
        } else {
            alert('Please select a valid .csv or .xlsx file.');
            fileInput.value = ''; // Reset
            dropZoneText.innerHTML = `Drag & drop your file here, or <span class="browse-link">browse</span>`;
            uploadBtn.disabled = true;
        }
    }

    // --- 3. Form Submission (AJAX) ---
    uploadForm.addEventListener('submit', (e) => {
        e.preventDefault();

        // 1. Hide Upload Section
        uploadSection.classList.add('hidden');
        
        // 2. Show Processing Animation
        processingSection.classList.remove('hidden');

        // Create FormData from form element
        const formData = new FormData(uploadForm);

        // First step: upload the dataset
        fetch('/inspect/upload_dataset', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Upload failed') });
            }
            return response.json();
        })
        .then(data => {
            // Second step: run the analysis
            return fetch('/inspect/analyse_dataset');
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.message || 'Analysis failed') });
            }
            return response.json();
        })
        .then(data => {
            // 3. Hide Processing Animation
            processingSection.classList.add('hidden');
            
            // 4. Show Results Area
            resultsSection.classList.remove('hidden');
    
// inject analysis data from backend to node

            // Inject the Pandas DataFrame HTML Tables
            document.getElementById('dataframe-1').innerHTML = data.summary_table;
            document.getElementById('dataframe-2').innerHTML = data.segment_table;

            // Inject the Base64 Matplotlib charts
            document.getElementById('chart-1').innerHTML = `<img src="data:image/png;base64,${data.pie_chart}" alt="RFM Distribution Pie Chart" style="max-width: 100%; height: auto; border-radius: 8px;">`;
            document.getElementById('chart-2').innerHTML = `<img src="data:image/png;base64,${data.bar_chart}" alt="RFM Distribution Bar Chart" style="max-width: 100%; height: auto; border-radius: 8px;">`;
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
            // Reset the UI back to the upload state
            processingSection.classList.add('hidden');
            uploadSection.classList.remove('hidden');
        });
    });

    // --- 4. Lightbox Modal Functionality ---
    const modalOverlay = document.getElementById('lightbox-modal');
    const modalContentArea = document.getElementById('modal-content-area');
    const modalClose = document.getElementById('modal-close');

    function openModal(htmlContent) {
        modalContentArea.innerHTML = htmlContent;
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        modalOverlay.classList.remove('active');
        modalContentArea.innerHTML = '';
        document.body.style.overflow = '';
    }

    modalClose.addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) closeModal();
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });

    // Handle card click events to expand in full-screen modal
    document.addEventListener('click', (e) => {
        const card = e.target.closest('.results-wrapper .chart-card');
        if (!card) return;

        // Check if it's the DataFrame card
        const table = card.querySelector('.dataframe-container table');
        if (table) {
            const titleElement = card.querySelector('h3');
            const title = titleElement ? titleElement.innerText : 'Dataset Overview';
            openModal(`
                <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 10px;">${title}</h3>
                <div class="modal-table-wrapper" style="overflow: auto; max-width: 100%; max-height: 90vh; font-size: 15px;">
                    ${table.outerHTML}
                </div>
            `);
            return;
        }

        // Check if it's a chart image card
        const img = card.querySelector('img');
        const titleElement = card.querySelector('h3');
        const title = titleElement ? titleElement.innerText : 'Visualization';
        if (img) {
            openModal(`
                <h3 style="margin-top: 0; margin-bottom: 20px; font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 10px;">${title}</h3>
                <div style="display: flex; justify-content: center; align-items: center;">
                    <img src="${img.src}" alt="${title}" style="max-width: 100%; max-height: 70vh; object-fit: contain; border-radius: 8px;">
                </div>
            `);
        }
    });

});

