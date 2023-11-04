// Uploading images (Front end -> Back end)
document.getElementById("uploadButton").addEventListener("click", function () {
    const imageInput = document.getElementById("imageInput");
    const formData = new FormData();

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
            })
            .catch((error) => {
                // Handle any errors
                console.error(error);
            });
    } else {
        // Handle the case where no files are selected
        console.log("No files selected.");
    }
});

function makePostReqeust_axios(url, data, f) {
    axios.post(url, data).then(f);
}

function makePostRequest(url, data, f) {
    let http = new XMLHttpRequest();    

    http.open('POST', url, true);
    http.setRequestHeader('Content-Type', 'application/json');

    http.onreadystatechange = function() {
        if(http.readyState == 4 && http.status == 200)  // if successful
            f(http.responseText)
    }
    http.send(JSON.stringify(data));
}

function handleSubmission() {
  let requestAddress = "http://127.0.0.1:8000";
  let input = document.getElementById("textInput").value;
   
    makePostRequest(
        requestAddress + '/textreturn',
        { "text": input },
        finished
    );
}

function finished(response) {
    let result = JSON.parse(response);
    console.log(result)
    let resultHTML = result["text"];

    document.getElementById("resultDiv").innerHTML = resultHTML;
}