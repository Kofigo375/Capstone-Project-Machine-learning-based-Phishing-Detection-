// Purpose - This file contains all the logic relevant to the extension, such as getting the URL and sending a JSON request to the server-side API.

// Function to send a JSON request to the server for processing
function sendRequest() {
    // Get the URL of the currently active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const currentUrl = tabs[0].url;
      
      // Display the URL being tested on the popup
      document.getElementById("p1").innerText = "The URL being tested is - " + currentUrl;
      console.log("displayed url");
      
      // Prepare the data to send in the JSON request
      const requestData = {
        url: currentUrl,
        html: document.documentElement.innerHTML
      };
  
      // Make a JSON POST request to the server-side API
      fetch("http://127.0.0.1:5000", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
      })
      .then(response => response.json())
      .then(data => {
        // Display the response from the server in the popup
        if (data.prediction === 1){
          document.getElementById("div1").innerText = "This website is Legitimate";
        }
        else{
          document.getElementById("div2").innerText = "This website is Phishing";

        }
      })
      .catch(error => {
        // Handle any errors that occur during the fetch request
        console.error("Error:", error);
      });
    });
    console.log("ruuning");
  }
  
  // Set up an event listener for the button click in the popup
  document.addEventListener('DOMContentLoaded', function() {
   
  
    // Get the URL of the currently active tab and display it on the popup
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const currentUrl = tabs[0].url;

      document.getElementById("p1").innerText = "The URL being tested is : " + currentUrl;
      sendRequest();
    });
  });


  