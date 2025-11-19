/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

 async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });
    // Handle the response
    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = '../index'
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            // Your code to handle form submission
            console.log(email);
            await loginUser(email, password)
        });
    }
    else{
      // test at index
      checkAuthentication();
      const price_filter = document.getElementById('price-filter');
      price_filter.innerHTML = '<option value="10">10</option><option value="50">50</option><option value="100">100</option><option value="All">All</option>'
    }
  });


function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-button');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
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
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
     if (response.ok) {
       //alert('Response Places OK: ' + response.statusText);
       const data = await response.json();
       displayPlaces(data)

    } else {
        alert('Failed to get places: ' + response.statusText);
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
            place_html += '<button class="details-button"><a href="place.html" id="details-button">View Details</a></button>'
            place_html += '</div>'
            place_list.innerHTML += place_html;
            console.log(place_list.innerHTML);
        });
}

document.getElementById('price-filter').addEventListener('change', (event) => {
    // Get the selected price value
    const place_list = document.getElementById('places-list');
    const price_list = document.querySelectorAll('.place-price');
    console.log(price_list)
    const max_price = event.target.value;
    console.log(max_price);
    let counter=0 
    for (const place_card of place_list.children) {
      let price_of_place = price_list[counter].textContent;
      console.log(price_of_place)
      price_of_place=price_of_place.substring(1);
      console.log(price_of_place);
      if (max_price != "All") {
        place_card.style.display = "none";
      }else{
        place_card.style.display = "block";
      }
      if (parseInt(price_of_place) > parseInt(max_price)) {
          place_card.style.display = "none";
      }else{
          place_card.style.display = "block";
      }
      
      counter += 1;
    }
    
    

    // Iterate over the places and show/hide them based on the selected price
});

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