document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('uploadForm');
    const imgForm = document.getElementById('imgForm');
    const csvFileInput = document.getElementById('csvFile'); ////
    const imgFileInput = document.getElementById('imgFile'); ////
    const fileNameDisplay = document.getElementById('fileName');
    const statusDisplay = document.getElementById('status');

    csvFileInput.addEventListener('change', function () {         
        const fileName = csvFileInput.files[0] ? csvFileInput.files[0].name : '';
        fileNameDisplay.textContent = fileName;
    });

    
    
    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const file = csvFileInput.files[0];
        const contentType = document.getElementById('contentType').value;
        
        if (!file) {
            statusDisplay.textContent = 'No file selected!';
            return;
            }
            
        const formData = new FormData();
        formData.append('csv', file);
        formData.append('contentType', contentType);

        fetch('http://127.0.0.1:8000/upload/csv/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            statusDisplay.textContent = 'File uploaded successfully!';
            console.log(data);
        })
        .catch(error => {
            statusDisplay.textContent = 'Failed to upload file!';
            console.error('Error:', error);
        });
    });

    // img upload (will be used for both icons and questions)
            
    imgFileInput.addEventListener('change', function () {         
        const fileNames = Array.from(imgFileInput.files).map(file => file.name).join(', '); // Get all file names
        fileNameDisplay.textContent = fileNames;
    });

    imgForm.addEventListener('submit', function (event) {
        event.preventDefault();
        
        const files = imgFileInput.files;
        const contentType = document.getElementById('imgContentType').value;
        
        if (files.length === 0) {
            statusDisplay.textContent = 'Please select image files (PNG, JPG, etc.).';
            return;
        }
            
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            if (files[i].type.startsWith('image/')) { 
                formData.append('img', files[i]);  // Append each file
            }
        }
        formData.append('contentType', contentType);
                    
        fetch('http://127.0.0.1:8000/upload/img/', {
            method: 'POST',
            body: formData,
            })
            .then(response => response.json())
            .then(data => {
                statusDisplay.textContent = 'File uploaded successfully!';
                console.log(data);
                })
                .catch(error => {
            statusDisplay.textContent = 'Failed to upload file!';
            console.error('Error:', error);
        });
    });
});



