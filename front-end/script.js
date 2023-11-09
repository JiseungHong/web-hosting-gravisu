// Uploading images (Front end -> Back end)
document.querySelectorAll('.upload-button').forEach(function(button) {
  button.addEventListener("click", function () {
    const imageInput = document.getElementById("fileSystem");
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
      .then((response) => response.json())
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
  });
});

document.querySelectorAll('.save-model-and-display-button').forEach(function(button) {
  button.addEventListener("click", function () {
    fetch("http://127.0.0.1:8000/upload-model", {
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
  });
});


// Following codes are the example codes for text return function.
function makePostReqeust_axios(url, data, f) {
  axios.post(url, data).then(f);
}

function makePostRequest(url, data, f) {
  let http = new XMLHttpRequest();

  http.open("POST", url, true);
  http.setRequestHeader("Content-Type", "application/json");

  http.onreadystatechange = function () {
    if (http.readyState == 4 && http.status == 200)
      // if successful
      f(http.responseText);
  };
  http.send(JSON.stringify(data));
}

function handleSubmission() {
  let requestAddress = "http://127.0.0.1:8000";
  let input = document.getElementById("textInput").value;

  makePostRequest(requestAddress + "/textreturn", { text: input }, finished);
}

function finished(response) {
  let result = JSON.parse(response);
  console.log(result);
  let resultHTML = result["text"];

  document.getElementById("resultDiv").innerHTML = resultHTML;
}
