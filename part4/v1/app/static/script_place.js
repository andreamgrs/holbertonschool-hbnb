/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const reviewButton = document.getElementById('review-button');
  reviewButton.addEventListener('click', function () {
    const place_id = getPlaceIdFromURL();
    window.location.href = 'add_review?id=' + place_id;
  });
});


function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');
  const loginLink = document.getElementById('login-button');

  if (!token) {
    addReviewSection.style.display = 'none';
    loginLink.style.display = 'block';
  } else {
    addReviewSection.style.display = 'block';
    loginLink.style.display = 'none';
  }
  placeId = getPlaceIdFromURL();
  fetchPlaceDetails(token, placeId);
  fetchReviews(token, placeId);
}

function getCookie(name) {
  // Function to get a cookie value by its name
  console.log(name);
  cookies = document.cookie.split(";")
  let cookie_name = name + "=";
  console.log(cookies);
  for (let i = 0; i < cookies.length; i++) {
    let c = cookies[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(cookie_name) == 0) {
      console.log("the return", c.substring(cookie_name.length, c.length))
      return c.substring(cookie_name.length, c.length);
    }
  }
}

/* GET THE ID FROM PLACE URL */
function getPlaceIdFromURL() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  const placeId = urlParams.get('id');
  console.log(placeId)
  return placeId
}

/*FETCH PLACE DETAILS */
async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails
  //  function
  // Make a GET request to fetch places data
  const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
  if (response.ok) {
    //alert('Response Places OK: ' + response.statusText);
    const data = await response.json();
    displayPlaceDetails(data)

  } else {
    alert('Failed to get place details: ' + response.statusText);
  }
}

/*POPULATE PLACE DETAILS */
function displayPlaceDetails(place) {
  // Clear the current content of the place details section
  // Create elements to display the place details (name, description, price, amenities and reviews)
  // Append the created elements to the place details section
  const place_details = document.getElementById('place-details');
  place_details.innerHTML = " ";
  let place_html = '<div class="place-each-card">';
  place_html += `<p class="place-title"><b>${place.title}</b></p>`;
  place_html += `<img src="/static/images/${place.id}.jpg" class="place-image">`;
  place_html += "<p> Owner: " + place.owner.first_name + " " + place.owner.last_name + "</p>";
  place_html += "<p> Description: " + place.description + "</p>";
  place_html += "<p> Price per night $" + place.price + "</p>";
  place_html += "<p> Amenities: ";
  console.log(place.amenities);
  place.amenities.forEach(amenity => {
    console.log(amenity);
    place_html += amenity.name + ", ";
  });
  place_html = place_html.slice(0, -2);
  place_html += "</p>";
  place_html += '</div>';
  place_details.innerHTML += place_html;
  console.log(place_details.innerHTML);
}

/* LIST OF REVIEWS INSIDE EACH PLACE */
async function fetchReviews(token, placeId) {
  // Make a GET request to fetch places data
  const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews/places/${placeId}/reviews`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
  if (response.ok) {
    //alert('Response Places OK: ' + response.statusText);
    const data = await response.json();
    displayReviews(data)

  } else {
    alert('Failed to get all reviews: ' + response.statusText);
  }
}

async function displayReviews(reviews) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list
  console.log(reviews)
  const review_list = document.getElementById('reviews-list');
  review_list.innerHTML = " Reviews "
  for (const review of reviews) {
    const userName = await getUsernameFromId(review.user_id)
    console.log(userName)
    let review_html = '<div class="review-card">';
    /* star rating function */
    let stars = '';
    const maxStars = 5;
    for (let starNumber = 0; starNumber < maxStars; starNumber++) {
      if (starNumber < review.rating) stars += '★';
      else stars += '☆';
    }
    review_html += `<div class="star-rating">${stars}</div>`;
    /* end of star rating function */
    review_html += "<p><b>" + userName + "</b></p>";
    review_html += "<p>" + review.text + "</p>";

    review_html += '</div>'
    review_list.innerHTML += review_html;
    console.log(review_list.innerHTML);
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
    console.log(data)
    username = data.user.first_name + ' ' + data.user.last_name;
    console.log(username)
    return username
  } else {
    alert('Failed to get owner: ' + response.statusText);
  }

}