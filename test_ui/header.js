function updateAuthLinks() {
  const authLinks = document.getElementById('auth-links');
  if (!authLinks) return;
  const token = localStorage.getItem('access_token');
  if (token) {
    authLinks.innerHTML = '<a href="my-cars.html">Your Cars</a> | <a href="#" id="logout-link">Logout</a>';
    const logout = document.getElementById('logout-link');
    logout.addEventListener('click', function(e) {
      e.preventDefault();
      localStorage.removeItem('access_token');
      updateAuthLinks();
    });
  } else {
    authLinks.innerHTML = '<a href="login.html">Login</a> | <a href="signup.html">Register</a>';
  }
}

document.addEventListener('DOMContentLoaded', updateAuthLinks);
