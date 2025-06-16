let Maximum_Classes = [];
let current_column = 1;
let current_class = 1;
let imgDrop = [];
let modelDrop;
let modelUpload = new DataTransfer();

const dragDropImg = document.querySelector(".imgFileBox");
const dragDropModel = document.querySelector(".modelFileBox");

// Enable buttons when files are valid
let userFile1 = document.getElementById("fileSystem1");
let userFile2 = document.getElementById("fileSystem2");
let submitButton1 = document.getElementsByClassName("upload-button")[0];
let submitButton2 = document.getElementsByClassName("save-model-button")[0];
let runButton = document.getElementsByClassName("run-button")[0];

userFile1.addEventListener("change", stateHandle);
userFile2.addEventListener("change", stateHandle);

function stateHandle() {
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

dragDropImg.addEventListener("dragover", (event) => {
  event.preventDefault();
  document.getElementById("img_drop").innerHTML = "Release to upload";
});

dragDropImg.addEventListener("dragleave", () => {
  document.getElementById("img_drop").innerHTML =
    "Drag and drop files here<br>OR";
});

dragDropImg.addEventListener("drop", (event) => {
  event.preventDefault();
  imgDrop = event.dataTransfer.files;
  document.getElementById("img_drop").innerHTML =
    "Drag and drop files here<br>OR";
  submitButton1.disabled = false;
});

dragDropModel.addEventListener("dragover", (event) => {
  event.preventDefault();
  document.getElementById("model_drop").innerHTML = "Release to upload";
});

dragDropModel.addEventListener("dragleave", () => {
  document.getElementById("model_drop").innerHTML =
    "Drag and drop files here<br>OR";
});

dragDropModel.addEventListener("drop", (event) => {
  event.preventDefault();
  modelDrop = event.dataTransfer.files;
  for (let i = 0; i < modelDrop.length; i++) {
    modelUpload.items.add(modelDrop[i]);
  }
  document.getElementById("model_drop").innerHTML =
    "Drag and drop files here<br>OR";
  submitButton2.disabled = false;
});

// Upload images (Front end -> Back end)
function function1(e) {
  e.preventDefault();

  current_column = 0;
  current_class = 0;

  // const imageInput = document.getElementById("fileSystem");
  const imageInput = document.querySelector(".imageClass");
  const formData = new FormData();
  const imageNumberDiv = document.getElementById("imageNumber");
  imageNumberDiv.textContent = "Uploading images...";

  // Check if any files are selected
  const imageInputLen = imageInput.files.length;
  const imgDropLen = imgDrop.length;
  if (imageInputLen > 0 || imgDropLen > 0) {
    // Append each selected image file to the FormData object
    if (imageInputLen > 0) {
      for (let i = 0; i < imageInputLen; i++) {
        formData.append("files", imageInput.files[i]);
      }
    }
    if (imgDropLen > 0) {
      for (let i = 0; i < imgDropLen; i++) {
        formData.append("files", imgDrop[i]);
      }
    }

    // Send the FormData object to the server using a POST request
    fetch("http://110.76.86.172:8000/upload-images", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        // Handle the server's response, e.g., display a success message
        imageNumberDiv.textContent = `You have uploaded ${
          imageInputLen + imgDropLen
        } images.`;
        console.log(data);
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
  if (fileInput.files.length !== 0) {
    for (let i = 0; i < fileInput.files.length; i++) {
      modelUpload.items.add(fileInput.files[i]);
    }
  }

  if (modelUpload.length === 0) {
    console.error("No file selected.");
    return;
  }

  const modelLoadingDiv = document.getElementById("modelLoading");
  modelLoadingDiv.textContent = "Uploading model...";

  // Save the model.
  const formData = new FormData();
  const zipFile = modelUpload.files[0];
  formData.append("zipFile", zipFile);

  // Send the FormData object to the server using a POST request
  fetch("http://110.76.86.172:8000/upload-model", {
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
      modelLoadingDiv.textContent = "Model upload complete.";
      runButton.disabled = false;
    })
    .catch((error) => {
      console.error("Fetch error:", error.message);
    });
}

let left_arrow = document.getElementsByClassName("left_arrow")[0];
let right_arrow = document.getElementsByClassName("right_arrow")[0];

// Run GradCam++.
function function3(e) {
  e.preventDefault();

  runButton.textContent = "Running...";
  runButton.disabled = true;
  submitButton1.disabled = true;
  submitButton2.disabled = true;

  fetch("http://110.76.86.172:8000/run-gradcam", {
    //////////////////////////// test
    // fetch("http://110.76.86.172:8000/test", {
    //////////////////////////// test
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
      console.log("Gra-Visu running...");
      const imagePaths = data.image_paths;
      const baseUrl = "http://110.76.86.172:8000/heatmap/"; // Base URL for serving images

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;
        const imgElement = document.querySelector(
          ".result" + (index + 1) + " .mask .im"
        );
        if (imgElement) {
          imgElement.src = imageUrl;
          console.log("Image src updated for", imgElement);
        } else {
          console.log("No img element found for result" + (index + 1));
        }
      });

      Maximum_Classes = data.max_value;
      current_column = 1;
      current_class = 0;

      document.getElementById("current_column").textContent = current_column;
      max_column = Maximum_Classes[current_class];
      if (max_column == 0 || max_column == 1) {
        document.getElementById("max_column").textContent = 1;
        left_arrow.disabled = true;
        right_arrow.disabled = true;
      } else {
        document.getElementById("max_column").textContent = max_column;
        left_arrow.disabled = true;
        right_arrow.disabled = false;
      }

      const drop_down = document.querySelector(".inst_text .inst_num");
      drop_down.value = current_class + 1;
      drop_down.max = Maximum_Classes.length;
      // document.getElementById(
      //   "class_num"
      // ).textContent += ` (max: ${Maximum_Classes.length})`;

      const chartElement = document.querySelector(".chart .chart_content");
      if (chartElement) {
        chartElement.src = baseUrl + data.histogram;
        console.log("Chart src updated for", chartElement);
      } else {
        console.log("No chart element found for chart_element");
      }

      // Display duration
      alert(`Model processing time: ${data.duration}`);

      runButton.textContent = "Run Gra-Visu";
      runButton.disabled = false;
      submitButton1.disabled = false;
      submitButton2.disabled = false;
    })
    .catch((error) => {
      console.error(error);
    });
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
      console.log("Gra-Visu running...");
      const imagePaths = data.image_paths;
      const baseUrl = "http://110.76.86.172:8000/heatmap/"; // Base URL for serving images

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;
        const imgElement = document.querySelector(
          ".result" + (index + 1) + " .mask .im"
        );
        if (imgElement) {
          imgElement.src = imageUrl;
          console.log("Image src updated for", imgElement);
        } else {
          console.log("No img element found for result" + (index + 1));
        }
      });

      Maximum_Classes = data.max_value;
      current_column = 1;
      current_class = 0;

      document.getElementById("current_column").textContent = current_column;
      max_column = Maximum_Classes[current_class];
      if (max_column == 0 || max_column == 1) {
        document.getElementById("max_column").textContent = 1;
        left_arrow.disabled = true;
        right_arrow.disabled = true;
      } else {
        document.getElementById("max_column").textContent = max_column;
        left_arrow.disabled = true;
        right_arrow.disabled = false;
      }

      const drop_down = document.querySelector(".inst_text .inst_num");
      drop_down.value = current_class + 1;
      drop_down.max = Maximum_Classes.length;
      // document.getElementById(
      //   "class_num"
      // ).textContent += ` (max: ${Maximum_Classes.length})`;

      const chartElement = document.querySelector(".chart .chart_content");
      if (chartElement) {
        chartElement.src = baseUrl + data.histogram;
        console.log("Chart src updated for", chartElement);
      } else {
        console.log("No chart element found for chart_element");
      }

      runButton.textContent = "Run Gra-Visu";
      runButton.disabled = false;
      submitButton1.disabled = false;
      submitButton2.disabled = false;
    })
    .catch((error) => {
      console.error(error);
    });
}

// Next Button
function move_next(e) {
  e.preventDefault();

  const maxColumn = document.getElementById("max_column").textContent;

  // Error handling for boundary values.
  if (current_column >= maxColumn) {
    right_arrow.disabled = true;
  } else {
    right_arrow.disabled = false;
    if (current_column === 1 && maxColumn > 1) {
      left_arrow.disabled = false;
    }
    current_column = current_column + 1;
    if (current_column == maxColumn) {
      right_arrow.disabled = true;
    }
  }

  fetch("http://110.76.86.172:8000/next-button", {
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
      const baseUrl = "http://110.76.86.172:8000/heatmap/"; // Base URL for serving images

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;
        const imgElement = document.querySelector(
          ".result" + (index + 1) + " .mask .im"
        );
        if (imgElement) {
          imgElement.src = imageUrl;
          console.log("Image src updated for", imgElement);
        } else {
          console.log("No img element found for result" + (index + 1));
        }
      });

      document.getElementById("current_column").textContent = current_column;
    })
    .catch((error) => {
      console.error(error);
    });
}

// Previous Button
function move_prev(e) {
  e.preventDefault();

  const maxColumn = document.getElementById("max_column").textContent;

  // Error handling for boundary values.
  if (current_column <= 1) {
    left_arrow.disabled = true;
  } else {
    left_arrow.disabled = false;
    if (current_column == maxColumn && maxColumn > 1) {
      right_arrow.disabled = false;
    }
    current_column = current_column - 1;
    if (current_column === 1) {
      left_arrow.disabled = true;
    }
  }

  fetch("http://110.76.86.172:8000/prev-button", {
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
      const baseUrl = "http://110.76.86.172:8000/heatmap/"; // Base URL for serving images

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;
        const imgElement = document.querySelector(
          ".result" + (index + 1) + " .mask .im"
        );
        if (imgElement) {
          imgElement.src = imageUrl;
          console.log("Image src updated for", imgElement);
        } else {
          console.log("No img element found for result" + (index + 1));
        }
      });

      document.getElementById("current_column").textContent = current_column;
    })
    .catch((error) => {
      console.error(error);
    });
}

function handleInputChange(event) {
  const number = parseInt(event.target.value, 10);
  const formData = new FormData();
  formData.append("class_num", number);

  fetch("http://110.76.86.172:8000/class-dropdown", {
    method: "POST",
    body: formData,
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
      const baseUrl = "http://110.76.86.172:8000/heatmap/"; // Base URL for serving images

      // Loop through each imagePath and set it as the background for the corresponding result div
      imagePaths.forEach((path, index) => {
        // Construct the full image URL
        const imageUrl = baseUrl + path;
        const imgElement = document.querySelector(
          ".result" + (index + 1) + " .mask .im"
        );
        if (imgElement) {
          imgElement.src = imageUrl;
          console.log("Image src updated for", imgElement);
        } else {
          console.log("No img element found for result" + (index + 1));
        }
      });

      current_column = 1;
      current_class = number - 1;

      console.log(
        "current class",
        current_class,
        "current column",
        current_column,
        Maximum_Classes
      );
      max_column = Maximum_Classes[current_class];
      document.getElementById("current_column").textContent = current_column;
      if (max_column == 0 || max_column == 1) {
        document.getElementById("max_column").textContent = 1;
        left_arrow.disabled = true;
        right_arrow.disabled = true;
      } else {
        document.getElementById("max_column").textContent = max_column;
        left_arrow.disabled = true;
        right_arrow.disabled = false;
      }

      const chartElement = document.querySelector(".chart .chart_content");
      if (chartElement) {
        chartElement.src = baseUrl + data.histogram;
        console.log("Chart src updated for", chartElement);
      } else {
        console.log("No chart element found for chart_element");
      }
    })
    .catch((error) => {
      console.error(error);
    });
}
