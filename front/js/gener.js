// This file contain functions I'm using in the rest of the files


// Display a success notification using Toastify
function showSuccessNotification(message) {
  Toastify({
    text: message,
    duration: 3500,
    destination: "https://github.com/apvarun/toastify-js",
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background: "linear-gradient(to right, #00b09b, #96c93d)",
    },
    onClick: function () { } // Callback after click
  }).showToast();
}

// Display an error notification using Toastify
function showErrorNotification(message) {
  Toastify({
    text: message,
    duration: 3000,
    destination: "https://github.com/apvarun/toastify-js",
    newWindow: true,
    close: true,
    gravity: "top", // `top` or `bottom`
    position: "right", // `left`, `center` or `right`
    stopOnFocus: true, // Prevents dismissing of toast on hover
    style: {
      background: "linear-gradient(to right, #ee4318, #efef0c   )",
    },
    onClick: function () { } // Callback after click
  }).showToast();
}

// Token Decoding
function parseJwt(token) {
  var base64Url = token.split('.')[1];
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function (c) {
    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(''));

  return JSON.parse(jsonPayload);
}

// Show error tostify and take to other page
const changePageError = (page, message) => {
  showErrorNotification(message)
  setTimeout(() => {
    window.location.href = page;
  }, 2000)
}

// Show success tostify and take to other page
const changePageSuccess = (page, message) => {
  showSuccessNotification(message)
  setTimeout(() => {
    window.location.href = page;
  }, 2000)
}

// Display username in top of page
const display_username = () => {
  return null
}