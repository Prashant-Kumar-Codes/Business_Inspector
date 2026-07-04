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
    dropZone.addEventListener('click', () => {
        fileInput.click();
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
        })
        .catch(error => {
            alert(`Error: ${error.message}`);
            // Reset the UI back to the upload state
            processingSection.classList.add('hidden');
            uploadSection.classList.remove('hidden');
        });
    });

});
