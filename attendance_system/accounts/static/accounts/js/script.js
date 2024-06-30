function previewImage(event) {
    var reader = new FileReader();
    reader.onload = function () {
      var output = document.getElementById('uploadPreview');
      output.innerHTML = '<img src="' + reader.result + '" alt="Preview">';
      output.style.display = 'block'; // Show the box frame
    };
    reader.readAsDataURL(event.target.files[0]);
  }
  