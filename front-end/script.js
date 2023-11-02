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