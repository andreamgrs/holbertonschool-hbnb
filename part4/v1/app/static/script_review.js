/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

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
            console.log(reviewText)
            // Make AJAX request to submit review
            console.log(rating_filter.value)
            response = submitReview(token, placeId, reviewText, parseInt(rating_filter.value))
            // Handle the response
            console.log(response)
            handleResponse(response)
        });
    }
  });

async function submitReview(token, placeId, reviewText, rating) {
    // Make a POST request to submit review data
    // Include the token in the Authorization header
    // Send placeId and reviewText in the request body
    // Handle the response
    const data_send = {
        place_id: `${placeId}`,
        text: `${reviewText}`,
        rating
    };
    console.log(data_send)
    console.log(JSON.stringify(data_send))
    const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data_send)
    })

    // Handle the response
    console.log(response.status, response.ok)
    return response
}

function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
    } else {
        alert('Failed to submit review');
    }
}


function checkAuthentication() {
    const token = getCookie('token');

    if (!token) {
        window.location.href = 'index.html';
    } 
    return token;
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

