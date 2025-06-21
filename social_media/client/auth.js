const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const messageBox = document.getElementById('message');

const API_USERS = 'http://127.0.0.1:8000/api-users';

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const res = await fetch(`${API_USERS}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (res.ok && data.token) {
    localStorage.setItem('token', data.token);
    window.location.href = 'home.html';
  } else {
    messageBox.textContent = data.error || 'Credenziali non valide.';
  }
});

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById('reg-username').value;
  const password = document.getElementById('reg-password').value;
  const email = document.getElementById('reg-email').value;
  const bio = document.getElementById('reg-bio').value;

  const registrationData = {
    username,
    password,
    bio,
  };

  if (email) {
    registrationData.email = email;
  }

  const res = await fetch(`${API_USERS}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registrationData)
  });

  const data = await res.json();

  if (res.ok && data.id) {
    //Registrazione riuscita, segue login automatico
    const loginRes = await fetch(`${API_USERS}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const loginData = await loginRes.json();
    if (loginRes.ok && loginData.token) {
      localStorage.setItem('token', loginData.token);
      window.location.href = 'home.html';
    } else {
      messageBox.textContent = 'Registrazione riuscita, ma errore nel login.';
    }
  } else {
    messageBox.style.color = 'red';
    messageBox.textContent = JSON.stringify(data);
  }
});