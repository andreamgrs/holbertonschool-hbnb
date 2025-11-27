// Wait for page to load
document.addEventListener('DOMContentLoaded', () => {
  // Hide login link on the login page
  const loginLink = document.getElementById('login-button');
  loginLink.style.display = 'none';
  
  // Login when user clicks submit on the login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      await loginUser(email, password);
    });
  };    
});

async function loginUser(email, password) {
  // API call to login
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
    // Add the access token to cookies
    document.cookie = `token=${data.access_token}; path=/`;
    // Redirect to index page
    window.location.href = '../index';
  } else {
      let errorMessage = 'Login failed';
      try {
        const data = await response.json();
        if (data.error) {
          errorMessage = data.error;
        }
      } catch (err) {
      }
      alert(errorMessage);
  };
};



