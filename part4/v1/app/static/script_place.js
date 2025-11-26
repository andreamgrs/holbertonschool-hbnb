/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    const reviewButton = document.getElementById('review-button');
    reviewButton.addEventListener('click', function() {
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
}

function getCookie(name) {
    // Function to get a cookie value by its name
    console.log(name);
    cookies = document.cookie.split(";")
    let cookie_name = name + "=";
    console.log(cookies);
    for(let i = 0; i < cookies.length; i++) {
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
    place_details.innerHTML=" ";
    let place_html = '<div class="place-card">';
    place_html += "<p>" + place.title + "</p>";
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
async function fetchReviews(token) {
    // Make a GET request to fetch places data
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
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

function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
    const place_list = document.getElementById('places-list');
    place_list.innerHTML=" "
    places.forEach(place => {
            console.log(places);
            let place_html = '<div class="place-card">';
            place_html += "<p>" + place.title + "</p>";
            place_html += '<p class="place-price">' + "$" + place.price + "</p>";
            place_html += '<button class="details-button"><a href="place?id=' + place.id +'" id="details-button">View Details</a></button>'
            place_html += '</div>'
            place_list.innerHTML += place_html;
            console.log(place_list.innerHTML);
        });
}