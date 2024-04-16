/// Function to send the reviewsUrl to the Django server for processing
function sendUrlToServer(reviewsUrl) {
    fetch('http://localhost:8000/analyze_reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: reviewsUrl })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Send the results back to the popup for display after a delay
        setTimeout(() => {
            chrome.runtime.sendMessage({ type: 'results', data: data });
        }, 1000); // Adjust the delay as needed
    })  
    .catch((error) => {
        console.error('Error:', error);
        // Send an error message back to the popup
        chrome.runtime.sendMessage({ type: 'error', message: error.message });
    });
}
function sendSubscriptionEmail(email, price, productName) {
    fetch('http://localhost:8000/send_email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, price: price, productName: productName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Handle success response
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle error
    });
}


// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.type === 'amazonUrl') {
        // Received the URL from the popup, send it to the server for processing
        sendUrlToServer(message.url);
    }
});
