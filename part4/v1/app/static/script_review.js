// Wait for page to load
document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();
  const rating_filter = document.getElementById('rating');
  rating_filter.innerHTML = '<option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option>'

  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      // Get review text from form
      const reviewText = document.getElementById('review').value;
      // Make AJAX request to submit review
      const response = await submitReview(token, placeId, reviewText, parseInt(rating_filter.value))
      // Handle the response
      handleResponse(response)
    });
  };
});

async function submitReview(token, placeId, reviewText, rating) {
  // Convert data to correct format
  const data_send = {
    place_id: `${placeId}`,
    text: `${reviewText}`,
    rating
  };

  // Make a POST request to submit review data
  const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(data_send)
  });

  return response;
}

function handleResponse(response) {
  if (response.ok) {
    alert('Review submitted successfully!'); 
  } else {
    alert('Failed to submit review');
  }
    // Clear the form
    const reviewForm = document.getElementById('review-form');
    reviewForm.reset();
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button');

  if (!token) {
    // Redirect to index page
    window.location.href = 'index';
  } else {
    loginLink.style.display = 'none';
  }
  return token;
}

// Function to get a cookie value by its name
function getCookie(name) {
  // Get cookie string and split into list of cookies
  cookies = document.cookie.split(";")
  let cookie_name = name + "=";
  // Iterate through cookies
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i];
    // Remove leading spaces
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    // Check if cookie starts with cookie_name
    if (c.indexOf(cookie_name) == 0) {
      // Return everything after the cookie name 
      // i.e. value of the cookie
      return c.substring(cookie_name.length, c.length);
    }
  }
}

function getPlaceIdFromURL() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const placeId = urlParams.get('id');
  return placeId
}


