/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
  });


function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        placeId = getPlaceIdFromURL();
        fetchPlaceDetails(token, placeId);
    }
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
    // Handle the response and pass the data to displayPlaceDetails function
}

/*POPULATE PLACE DETAILS */
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
}
