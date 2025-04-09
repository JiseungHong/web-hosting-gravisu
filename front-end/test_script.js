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
    // Display the duration in a pop-up message
    console.log(`Time taken: ${data.duration}`);
    // Handle the rest of the data (e.g., image paths, max value, histogram)
    console.log(data);
  })
  .catch((error) => {
    console.error("Fetch error:", error.message);
  });
