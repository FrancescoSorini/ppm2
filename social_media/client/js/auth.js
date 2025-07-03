const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const messageBox = document.getElementById('message');
const API_USERS = window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000/api-users'
  : 'https://web-production-aa257.up.railway.app/api-users';


// Salva il token in un cookie
function setTokenCookie(token) {
  document.cookie = `token=${token}; path=/;`;
}


// Cancella eventuale cookie esistente
function clearTokenCookie() {
  document.cookie = "token=; Max-Age=0; path=/;";
}


// LOGIN
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearTokenCookie(); // rimuovi eventuali token precedenti

  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const res = await fetch(`${API_USERS}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (res.ok && data.token) {
    setTokenCookie(data.token);
    window.location.href = '/home/';
  } else {
    messageBox.textContent = data.error || 'Credenziali non valide.';
  }
});


// REGISTRAZIONE + LOGIN AUTOMATICO
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  clearTokenCookie();

  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;
  const email = document.getElementById('reg-email').value;
  const bio = document.getElementById('reg-bio').value;

  const registrationData = { username, password };
  if (email) registrationData.email = email;
  if (bio) registrationData.bio = bio;

  const res = await fetch(`${API_USERS}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registrationData)
  });

  const data = await res.json();

  if (res.ok && data.id) {
    // login automatico dopo registrazione
    const loginRes = await fetch(`${API_USERS}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const loginData = await loginRes.json();
    if (loginRes.ok && loginData.token) {
      setTokenCookie(loginData.token);
      window.location.href = '/home/';
    } else {
      messageBox.textContent = 'Registrazione riuscita, ma login fallito.';
    }
  } else {
    messageBox.textContent = JSON.stringify(data);
  }
});
