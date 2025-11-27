// Wait for the page to load
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const reviewButton = document.getElementById('review-button');
  reviewButton.addEventListener('click', function () {
    const place_id = getPlaceIdFromURL();
    window.location.href = 'add_review?id=' + place_id;
  });
});

// Check user authentication
function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const loginLink = document.getElementById('login-button');

  // Hide add review and show login if user is not logged in
  if (!token) {
    addReviewSection.style.display = 'none';
    loginLink.style.display = 'block';
  } else {
    // Show add review and hide login
    addReviewSection.style.display = 'block';
    loginLink.style.display = 'none';
  }
  // Get place details and reviews regardless of authentication status
  placeId = getPlaceIdFromURL();
  fetchPlaceDetails(token, placeId);
  fetchReviews(token, placeId);
}

// Fetch the place details
async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch places data
  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  // Handle the response and pass the data to displayPlaces function
  if (response.ok) {
    //alert('Response Places OK: ' + response.statusText);
    const data = await response.json();
    displayPlaceDetails(data);
  } else {
    alert('Failed to get place details: ' + response.statusText);
  };
};

// Display the place details
function displayPlaceDetails(place) {
  // Append the created elements to the place details section
  // Clear the current content of the place details section
  const place_details = document.getElementById('place-details');
  place_details.innerHTML = " ";

  // Create html string to display the place details
  let place_html = '<div class="place-each-card">';
  place_html += `<p class="place-title"><b>${place.title}</b></p>`;
  place_html += `<img src="/static/images/${place.id}.jpg" class="place-image">`;
  place_html += "<p><b> Owner: </b>" + place.owner.first_name + " " + place.owner.last_name + "</p>";
  place_html += "<p><b> Description: </b> " + place.description + "</p>";
  place_html += "<p> Price per night $" + place.price + "</p>";
  place_html += "<p><b> Amenities: </b>";
  place.amenities.forEach(amenity => {
    place_html += amenity.name + ", ";
  });
  place_html = place_html.slice(0, -2); // remove extra ", "
  place_html += "</p>";
  place_html += '</div>';
  place_details.innerHTML += place_html;
}

// Fetch all the reviews for a place
async function fetchReviews(token, placeId) {
  // Make a GET request to fetch reviews associated with a place
  const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  // Handle the response and pass the data to displayReviews function
  if (response.ok) {
    const data = await response.json();
    displayReviews(data);
  } else {
    alert('Failed to get all reviews: ' + response.statusText);
  };
}

// Display the reviews in the reviews-list
async function displayReviews(reviews) {
  // Clear the current content of the reviews list
  const review_list = document.getElementById('reviews-list');
  review_list.innerHTML = '<p><class="place-reviews-title"><b>Reviews</b></p>';
  
  // Iterate over the reviews
  for (const review of reviews) {
    const userName = await getUsernameFromId(review.user_id)
    // Create a reveiw card div
    let review_html = '<div class="review-card">';
    
    /* Convert rating to stars */
    let stars = '';
    const maxStars = 5;
    for (let starNumber = 0; starNumber < maxStars; starNumber++) {
      if (starNumber < review.rating) stars += '★';
      else stars += '☆';
    }
    review_html += `<div class="star-rating">${stars}</div>`;
    
    review_html += "<p><b>" + userName + "</b></p>";
    review_html += `<p class="review-text">${review.text}</p>`;
    review_html += '</div>';
    review_list.innerHTML += review_html;
  };
}

/* Get owner of review by user id */
async function getUsernameFromId(userId) {
  // Make a GET request to fetch places data
  const response = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
    method: 'GET'
  });
  if (response.ok) {
    const data = await response.json();
    username = data.user.first_name + ' ' + data.user.last_name;
    return username;
  } else {
    alert('Failed to get owner: ' + response.statusText);
  }
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

// Get place id from query param in URL
function getPlaceIdFromURL() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const placeId = urlParams.get('id');
  return placeId
}