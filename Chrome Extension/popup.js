// Function to get the URL of the active tab
function getActiveTabURL() {
    return new Promise((resolve, reject) => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs.length > 0) {
                resolve(tabs[0].url);
            } else {
                reject(new Error("No active tab found"));
            }
        });
    });
}

let receiveAlerts = true; 

// Function to send the reviewsUrl to the background script for processing
function sendUrlToBackground(reviewsUrl) {
    chrome.runtime.sendMessage({ type: 'amazonUrl', url: reviewsUrl });
}
// Function to send the subscription details to the background script for processing
function sendSubscriptionDetails(email, price) {
    console.log('Sending subscription details:', email, price);
    chrome.runtime.sendMessage({ type: 'subscribe', email: email, price: price });
}

async function subscribeToAlerts() {
    // Get the email input value
    const email = document.getElementById('emailInput').value;
    
    // Fetch the current price of the product
    const { price, productName } = await getProductDetails();

    // Send the subscription details to the background script for processing
    sendSubscriptionDetails(email, price, productName);

    if (receiveAlerts) {
        // Display the price in the popup
        document.getElementById('currentPrice').textContent = price;

        // Provide feedback to the user
        document.getElementById('message').textContent = "You have subscribed to price alerts.";
    } else {
        document.getElementById('message').textContent = "You have unsubscribed from price alerts.";
    }
}


document.addEventListener('DOMContentLoaded', function() {
    const subscribeButton = document.getElementById('subscribeButton');
    if (subscribeButton) {
        subscribeButton.addEventListener('click', subscribeToAlerts);
    }
});



async function getProductDetails() {
    try {
        const url = await getActiveTabURL(); // Get the URL of the active tab
        const response = await fetch(url); // Fetch data from the URL
        const text = await response.text(); // Get the text content of the response
        const parser = new DOMParser(); // Create a new DOMParser instance
        const htmlDocument = parser.parseFromString(text, 'text/html'); // Parse the text content as HTML
        const priceElement = htmlDocument.querySelector('span.a-price-whole');
        const productNameElement = htmlDocument.querySelector('#productTitle'); // Assuming '#productTitle' is the ID of the element containing the product name
        const price = priceElement ? priceElement.textContent.trim() : 'Price not found'; // Get the price or a message if not found
        const productName = productNameElement ? productNameElement.textContent.trim() : 'Product name not found'; // Get the product name or a message if not found
        return { price, productName }; // Return an object with the price and product name
    } catch (error) {
        console.error('Error fetching product details:', error); // Log any errors that occur
        return null; // Return null in case of an error
    }
}



// Call getCurrentPriceAndDisplay when the popup is loaded
document.addEventListener('DOMContentLoaded', getCurrentPriceAndDisplay);

    // Function to fetch the current price from Amazon using the URL of the active tab
async function getCurrentPriceAndDisplay() {
    try {
        const { price } = await getProductDetails(); // Fetch the current price
        document.getElementById('currentPrice').textContent = price; // Display the price in the popup
    } catch (error) {
        console.error('Error fetching current price:', error);
    }
}




// Check if the current page is an Amazon page
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const activeTabURL = await getActiveTabURL();

        if (!activeTabURL.includes("amazon.in")) {
            // Display a message in the popup if the current page is not an Amazon page
            document.getElementById('message').textContent = "This is not an Amazon page.";
            return;
        }

        // Modify the URL to get the reviews page URL
        let urlParts = activeTabURL.split('/');
        let productId = urlParts[urlParts.indexOf('dp') + 1];
        let baseUrl = urlParts.slice(0, urlParts.indexOf('dp')).join('/');
        let reviewsUrl = `${baseUrl}/product-reviews/${productId}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews`;

        // Send the reviewsUrl to the background script for processing
        sendUrlToBackground(reviewsUrl);
    } catch (error) {
        console.error("Error getting active tab URL:", error);
    }
});


// Update the chart with the results
function updatePieChart(positivePercentage, negativePercentage) {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Positive', 'Negative'],
            datasets: [{
                label: 'Sentiment Analysis',
                data: [positivePercentage, negativePercentage],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)', // Green for Positive
                    'rgba(255, 99, 132, 0.2)' // Red for Negative
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            //maintainAspectRatio: false
        }
    });
}

// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    console.log("message recevied:" ,message)
    if (message.type === 'results') {
        console.log("Received results:", message.data);
        // Update the popup with the sentiment analysis results
        document.getElementById('positivePercentage').textContent = message.data.positive_percentage;
        document.getElementById('negativePercentage').textContent = message.data.negative_percentage;

        // Update the pie chart with the results
        updatePieChart(message.data.positive_percentage, message.data.negative_percentage);
    } else if (message.type === 'error') {
        console.log("Received error:", message.message);
        // Display an error message in the popup
        document.getElementById('message').textContent = message.message;
    }
});
