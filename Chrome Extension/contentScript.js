//contentscript.js

// Check if the current page is an Amazon product page
if (window.location.hostname.includes('amazon.in') && window.location.pathname.includes('/dp/')) {
    // Extract the required part of the URL
    let urlParts = window.location.href.split('/');
    let productId = urlParts[urlParts.indexOf('dp') + 1];
    let baseUrl = urlParts.slice(0, urlParts.indexOf('dp')).join('/');
    let reviewsUrl = `${baseUrl}/product-reviews/${productId}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews`;

    // Send the modified URL to the background script
    chrome.runtime.sendMessage({ type: 'amazonUrl', url: reviewsUrl });

    // Send a message to the popup indicating that the URL is being sent to the server
    chrome.runtime.sendMessage({ type: 'message', message: 'Sending URL to server' });
} else {
    // Display an error message in the popup if the current page is not an Amazon product page
    chrome.runtime.sendMessage({ type: 'invalidUrl' });
}
