document.addEventListener('DOMContentLoaded', function () {
  const uploadForm = document.getElementById('uploadForm');
  const csvFileInput = document.getElementById('csvFile');
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
});


async function logQuestions() {
  response = await fetch("http://127.0.0.1:8000/questions/smcq");
  movies = await response.json();
  // response = await fetch("http://127.0.0.1:8000/questions/mmcq");
  // movies = await response.json();
  response = await fetch("http://127.0.0.1:8000/questions/intg");
  movies = await response.json();
  console.log(movies);
}
