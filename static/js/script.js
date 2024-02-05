document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault();

    var formData = new FormData(this);

    fetch('/classify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = '<h3>Result:</h3><p>' + data.result + '</p>';
    })
    .catch(error => console.error('Error:', error));
});
