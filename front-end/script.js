// Upload images (Front end -> Back end)
function function1(e){
  e.preventDefault();

  // const imageInput = document.getElementById("fileSystem");
  const imageInput = document.querySelector('.imageClass');
  const formData = new FormData();
  const imageNumberDiv = document.getElementById("imageNumber");

  // Check if any files are selected
  if (imageInput.files.length > 0) {
    // Append each selected image file to the FormData object
    for (let i = 0; i < imageInput.files.length; i++) {
      formData.append("files", imageInput.files[i]);
    }

    // Send the FormData object to the server using a POST request
    fetch("http://127.0.0.1:8000/upload-images", {
      method: "POST",
      body: formData,
    })
    .then((response) => {return response.json();})
    .then((data) => {
      // Handle the server's response, e.g., display a success message
      console.log(data);
      imageNumberDiv.innerHTML = `You have uploaded ${imageInput.files.length} images.`;
    })
    .catch((error) => {
      console.error(error);
    });
  } else {
    // Handle the case where no files are selected
    console.log("No files selected.");
  }
}

// Upload Model
function function2(e){
  e.preventDefault();
  const fileInput = document.querySelector('.save-model-button');
  if (fileInput.files.length === 0) {
    console.error("No file selected.");
    return;
  }
  
  // Save the model.
  const formData = new FormData();
  const zipFile = fileInput.files[0];
  formData.append('zipFile', zipFile);

  // Send the FormData object to the server using a POST request
  fetch("http://127.0.0.1:8000/upload-model-zip", {
    method: "POST",
    body: formData,
  })
  .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then((data) => {
    // Data error handling.
    if (data.error) {
      throw new Error(data.error);
    }
  })
  .catch((error) => {
    console.error("Fetch error:", error.message);
  });
}

// Run GradCam++.
function function3(e){
  e.preventDefault();
  fetch("http://127.0.0.1:8000/run-gradcam", {
    method: "POST",
  })
  .then((response) => {
    if (response.status === 200) {
      return response.json(); // Parse JSON response
    } else {
      throw new Error("Failed to fetch image paths from the server.");
    }
  })
  .then((data) => {
    const imagePaths = data.image_paths;
    const baseUrl = "http://127.0.0.1:8000/heatmap/"; // Base URL for serving images

    // Create and display img elements for each image path
    const resultDiv = document.getElementById("resultDiv");
    resultDiv.innerHTML = "";

    for (let i = 0; i < imagePaths.length; i += 2) {
      // Create a row div to hold two images
      const rowDiv = document.createElement("div");
      rowDiv.className = "image-row"; // Add a class for styling

      for (let j = i; j < i + 2 && j < imagePaths.length; j++) {
        const imagePath = imagePaths[j];
        const imageUrl = baseUrl + imagePath;
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";
        img.style.width = "50%"; // Set the width to 50% for resizing
        img.style.height = "auto"; // Maintain the aspect ratio
        img.style.margin = "0"; // Reset margin

        rowDiv.appendChild(img);
      }

      resultDiv.appendChild(rowDiv);
    }
  })
  .catch((error) => {
    console.error(error);
  });
}

// Next Button
function move_next(e){
  e.preventDefault();
  fetch("http://127.0.0.1:8000/next-button", {
    method: "POST",
  })
  .then((response) => {
    if (response.status === 200) {
      return response.json(); // Parse JSON response
    } else {
      throw new Error("Failed to fetch image paths from the server.");
    }
  })
  .then((data) => {
    const imagePaths = data.image_paths;
    const baseUrl = "http://127.0.0.1:8000/heatmap/"; // Base URL for serving images

    // Create and display img elements for each image path
    const resultDiv = document.getElementById("resultDiv");
    resultDiv.innerHTML = "";

    for (let i = 0; i < imagePaths.length; i += 2) {
      // Create a row div to hold two images
      const rowDiv = document.createElement("div");
      rowDiv.className = "image-row"; // Add a class for styling

      for (let j = i; j < i + 2 && j < imagePaths.length; j++) {
        const imagePath = imagePaths[j];
        const imageUrl = baseUrl + imagePath;
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";
        img.style.width = "50%"; // Set the width to 50% for resizing
        img.style.height = "auto"; // Maintain the aspect ratio
        img.style.margin = "0"; // Reset margin

        rowDiv.appendChild(img);
      }

      resultDiv.appendChild(rowDiv);
    }
  })
  .catch((error) => {
    console.error(error);
  });
}

// Previous Button
function move_prev(e){
  e.preventDefault();
  fetch("http://127.0.0.1:8000/prev-button", {
    method: "POST",
  })
  .then((response) => {
    if (response.status === 200) {
      return response.json(); // Parse JSON response
    } else {
      throw new Error("Failed to fetch image paths from the server.");
    }
  })
  .then((data) => {
    const imagePaths = data.image_paths;
    const baseUrl = "http://127.0.0.1:8000/heatmap/"; // Base URL for serving images

    // Create and display img elements for each image path
    const resultDiv = document.getElementById("resultDiv");
    resultDiv.innerHTML = "";

    for (let i = 0; i < imagePaths.length; i += 2) {
      // Create a row div to hold two images
      const rowDiv = document.createElement("div");
      rowDiv.className = "image-row"; // Add a class for styling

      for (let j = i; j < i + 2 && j < imagePaths.length; j++) {
        const imagePath = imagePaths[j];
        const imageUrl = baseUrl + imagePath;
        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";
        img.style.width = "50%"; // Set the width to 50% for resizing
        img.style.height = "auto"; // Maintain the aspect ratio
        img.style.margin = "0"; // Reset margin

        rowDiv.appendChild(img);
      }

      resultDiv.appendChild(rowDiv);
    }
  })
  .catch((error) => {
    console.error(error);
  });
}