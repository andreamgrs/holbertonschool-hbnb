// Check authentication and display price filter once page is loaded
document.addEventListener('DOMContentLoaded', () => {
  checkAuthentication();
  const price_filter = document.getElementById('price-filter');
  price_filter.innerHTML = '<option value="10">10</option><option value="50">50</option><option value="100">100</option><option value="All">All</option>'
});

// Check user is authenticated
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button');

  // Hide login link if user is already logged in
  if (!token) {
    loginLink.style.display = 'block';
  } else {
    loginLink.style.display = 'none';
  }

  // Fetch places regardless of whether user is logged in
  fetchPlaces(token);
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

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  // Handle the response and pass the data to displayPlaces function
  if (response.ok) {
    const data = await response.json();
    displayPlaces(data)

  } else {
    alert('Failed to get places: ' + response.statusText);
  }
}

function displayPlaces(places) {
  const place_list = document.getElementById('places-list');
  // Clear the content of the places list
  place_list.innerHTML = " "
  // Iterate over the places
  places.forEach(place => {
    // Create a div for each place and add the place info
    // Use place_html string to prevent closing elements being added
    let place_html = '<div class="place-card">';
    place_html += "<p>" + place.title + "</p>";
    place_html += `<img src="/static/images/${place.id}.jpg" class="place-image">`;
    place_html += '<p class="place-price">' + "$" + place.price + "</p>";
    place_html += '<button class="details-button"><a href="place?id=' + place.id + '" id="details-button">View Details</a></button>'
    place_html += '</div>'
    // Add place html to the inner html
    place_list.innerHTML += place_html;
  });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
  const place_list = document.getElementById('places-list');
  const price_list = document.querySelectorAll('.place-price');
  // Get the selected max price from the price filter
  const max_price = event.target.value;
  
  // Iterate through the place cards
  let counter = 0 // Counter for price list
  for (const place_card of place_list.children) {
    // Get price from place card
    let place_price = price_list[counter].textContent;
    // Remove leading '$'
    place_price = place_price.substring(1);
    // Display place card if price filter is All or place price is less than max price
    if ((max_price == "All") || (parseInt(place_price) <= parseInt(max_price))) {
      place_card.style.display = "block";
    } else {
      place_card.style.display = "none";
    }
    counter += 1;
  }
});



