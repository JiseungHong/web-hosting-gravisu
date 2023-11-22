let Maximum_Classes = [];
let current_column = 0;
let current_class = 0;

// Enable buttons when files are valid
let userFile1 = document.getElementById("fileSystem1");
let userFile2 = document.getElementById("fileSystem2");
let submitButton1 = document.getElementsByClassName("upload-button")[0];
let submitButton2 = document.getElementsByClassName("save-model-button")[0];

userFile1.addEventListener("change", stateHandle);
userFile2.addEventListener("change", stateHandle);

function stateHandle() {
  console.log("working");
  if (userFile1.value !== "") {
    submitButton1.disabled = false;
  } else {
    submitButton1.disabled = true;
  }
  if (userFile2.value !== "") {
    submitButton2.disabled = false;
  } else {
    submitButton2.disabled = true;
  }
}

// Upload images (Front end -> Back end)
function function1(e) {
  e.preventDefault();

  current_column = 0;
  current_class = 0;

  // const imageInput = document.getElementById("fileSystem");
  const imageInput = document.querySelector(".imageClass");
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
      .then((response) => {
        return response.json();
      })
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
function function2(e) {
  e.preventDefault();

  current_column = 0;
  current_class = 0;

  const fileInput = document.getElementById("fileSystem2");
  if (fileInput.files.length === 0) {
    console.error("No file selected.");
    return;
  }

  const modelLoadingDiv = document.getElementById("modelLoading");
  modelLoadingDiv.innerHTML = "Uploading model...";

  // Save the model.
  const formData = new FormData();
  const zipFile = fileInput.files[0];
  formData.append("zipFile", zipFile);

  // Send the FormData object to the server using a POST request
  fetch("http://127.0.0.1:8000/upload-model", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      modelLoadingDiv.innerHTML = "Model upload complete.";
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
function function3(e) {
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

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;

        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";

        const maskDiv = document.querySelector(
          ".result" + (index + 1) + " .mask"
        );
        if (maskDiv) {
          console.log("good", maskDiv);
          maskDiv.innerHTML = "";
          maskDiv.appendChild(img);
          // maskDiv.innerHTML = `<img src="${imageUrl}" alt="Image description">`;
        } else {
          console.log("err!!", maskDiv);
        }
      });
    })
    .catch((error) => {
      console.error(error);
    });
}

let left_arrow = document.getElementsByClassName("left_arrow")[0];
let right_arrow = document.getElementsByClassName("right_arrow")[0];

// Next Button
function move_next(e) {
  e.preventDefault();

  let current_column = document.getElementById("current_column").value;
  let max_column = document.getElementById("max_column").value;

  // Error handling for boundary values.
  if (current_column >= Maximum_Classes[current_class]) {
    // TODO: error handling
  } else {
    current_column = current_column + 1;
  }

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

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;

        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";

        const maskDiv = document.querySelector(
          ".result" + (index + 1) + " .mask"
        );
        if (maskDiv) {
          console.log("good", maskDiv);
          maskDiv.innerHTML = "";
          maskDiv.appendChild(img);
          // maskDiv.innerHTML = `<img src="${imageUrl}" alt="Image description">`;
        } else {
          console.log("err!!", maskDiv);
        }
      });
    })
    .catch((error) => {
      console.error(error);
    });
}

// Previous Button
function move_prev(e) {
  e.preventDefault();

  // Error handling for boundary values.
  if (current_column <= 0) {
    // TODO: error handling
  } else {
    current_column = current_column - 1;
  }

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

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;

        const img = document.createElement("img");
        img.src = imageUrl;
        img.alt = "Image";

        const maskDiv = document.querySelector(
          ".result" + (index + 1) + " .mask"
        );
        if (maskDiv) {
          console.log("good", maskDiv);
          maskDiv.innerHTML = "";
          maskDiv.appendChild(img);
          // maskDiv.innerHTML = `<img src="${imageUrl}" alt="Image description">`;
        } else {
          console.log("err!!", maskDiv);
        }
      });
    })
    .catch((error) => {
      console.error(error);
    });
}
