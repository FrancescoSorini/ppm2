const BASE_API = window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : 'https://web-production-aa257.up.railway.app';

const API_POSTS = `${BASE_API}/api-posts`;
const API_USERS = `${BASE_API}/api-users`;
const postContainer = document.getElementById("post-container");




// Recupera il token dal cookie
function getToken() {
  const match = document.cookie.match(/(^| )token=([^;]+)/);
  return match ? match[2] : null;
}

// Controlla se l'utente è loggato
const token = getToken();
if (!token) {
  window.location.href = "index.html"; // reindirizza alla pagina di login se non c'è token
}
let currentUser = null;


// Funzione logout
function logout(message = null) {
  document.cookie = "token=; Max-Age=0; path=/"; // cancella il cookie token
  if (message) alert(message);
  window.location.href = "index.html";
}


// Mostra nome utente loggato
async function loadCurrentUser() {
  const res = await fetch(`${API_USERS}/me`, {
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) return logout("Sessione scaduta. Effettua il login.");

  currentUser = await res.json(); // 👈 salvalo come variabile globale
  document.getElementById("username-display").textContent = `@${currentUser.username}`;
}


// Carica tutti i post
async function fetchPosts() {
  const res = await fetch(`${API_POSTS}/posts`, {
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) return logout("Sessione scaduta.");
  const posts = await res.json();
  postContainer.innerHTML = "";

  // Sezione html per i post
  posts.forEach(post => {
    const div = document.createElement("div");
    div.classList.add("post");

    div.innerHTML = `
      <h3>
        <a href="profile.html?user=${encodeURIComponent(post.author)}">@${post.author}</a> - ${post.title}
      </h3>
      <p>${post.content}</p>
      <small>Creato il: ${new Date(post.created_at).toLocaleString()}</small>
      <p>❤️ ${post.likes_count} like</p>
    
      <button onclick="likePost('${post.id}')">Mi piace</button>
    
      <h4>Commenti:</h4>
      ${post.comments.map(c => `
        <div class="comment">
          <strong>
            <a href="profile.html?user=${encodeURIComponent(c.author)}">@${c.author}</a>:
          </strong> ${c.content}
          ${(c.author === currentUser.username || currentUser.is_staff) ? `
            <button 
                onclick="deleteComment(${c.id})" 
                title="Elimina commento"
                style="font-size: 0.8rem; padding: 2px 6px; margin-left: 5px;"
            >❌</button>
          ` : ""}
        </div>
      `).join('')}
    
      <textarea id="comment-${post.id}" placeholder="Scrivi un commento..."></textarea>
      <button onclick="addComment('${post.id}')">Invia commento</button>
    
      ${(currentUser.is_staff) ? `
        <button onclick="deletePost(${post.id})"> 
          Elimina post
        </button>
      ` : ""}
    `;

    // Aggiunge il post al container
    postContainer.appendChild(div);
  });
}


// Crea un nuovo post
async function createPost() {
  const title = document.getElementById("new-post-title").value.trim();
  const content = document.getElementById("new-post-content").value.trim();

  if (!title || !content) {
    alert("Inserisci sia titolo che contenuto.");
    return;
  }

  // Controlla se l'utente è loggato
  const res = await fetch(`${API_POSTS}/posts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`
    },
    body: JSON.stringify({ title, content })
  });

  if (res.status === 401) return logout();
  if (res.ok) {
    alert("Post pubblicato!");
    document.getElementById("new-post-title").value = "";
    document.getElementById("new-post-content").value = "";
    fetchPosts(); // ricarica i post
  } else {
    const error = await res.json();
    alert("Errore nella creazione del post:\n" + JSON.stringify(error));
  }
}


// Invio Like
async function likePost(slug) {
  const res = await fetch(`${API_POSTS}/${slug}/like`, {
    method: "POST",
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) return logout();
  fetchPosts();
}


// Invio Commento
async function addComment(slug) {
  const textarea = document.getElementById(`comment-${slug}`);
  const content = textarea.value;
  if (!content.trim()) return;

  const res = await fetch(`${API_POSTS}/${slug}/comments/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`
    },
    body: JSON.stringify({ content })
  });

  if (res.status === 401) return logout();
  textarea.value = "";
  fetchPosts();
}


// Cerca utenti
async function search() {
  const query = document.getElementById("search-input").value.trim();
  if (!query) return;

  const res = await fetch(`${API_USERS}/search/?q=${query}`, {
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) return logout();

  const users = await res.json();

  if (users.length > 0) {
    const target = users[0];
    const confirmVisit = confirm(`Utente trovato: @${target.username}\nVuoi visitare il suo profilo?`);
    if (confirmVisit) {
      window.location.href = `profile.html?user=${encodeURIComponent(target.username)}`;
    }
  } else {
    alert("Nessun utente trovato con quel nome.");
  }
}


// Profilo personale utente loggato
async function goToProfile() {
  const res = await fetch("${API_USERS}/me", {
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) {
    logout("Sessione scaduta.");
    return;
  }

  const user = await res.json();
  const username = encodeURIComponent(user.username);
  window.location.href = `profile.html?user=${username}`;
}


// Elimina commento
async function deleteComment(commentId) {
  const confirmDelete = confirm("Vuoi eliminare questo commento?");
  if (!confirmDelete) return;

  const res = await fetch(`${API_POSTS}/comments/${commentId}/delete`, {
    method: "DELETE",
    headers: { Authorization: `Token ${token}` }
  });

  if (res.ok) {
    fetchPosts(); // aggiorna la lista dei post
  } else {
    alert("Errore durante l'eliminazione del commento.");
  }
}

// Notifiche
async function fetchNotifications() {
  const res = await fetch("`${BASE_API}/api-notifications/", {
    headers: { Authorization: `Token ${token}` }
  });

  if (!res.ok) return;

  const data = await res.json();
  const unread = data.filter(n => !n.is_read);
  const badge = document.getElementById("notification-badge");
  const list = document.getElementById("notification-list");

  // Badge
  if (unread.length > 0) {
    badge.textContent = unread.length;
    badge.style.display = "inline";
  } else {
    badge.style.display = "none";
  }

  // Lista notifiche
  list.innerHTML = "";

  if (unread.length === 0) {
    list.innerHTML = "<li style='padding: 0.5rem;'>Nessuna nuova notifica</li>";
    return;
  }

  unread.forEach(n => {
    const li = document.createElement("li");
    li.style.padding = "0.5rem";
    li.style.borderBottom = "1px solid #eee";
    li.textContent = `[${new Date(n.created_at).toLocaleString()}] ${n.message}`;
    list.appendChild(li);
  });
}

async function toggleNotifications() {
  const dropdown = document.getElementById("notification-dropdown");
  const isVisible = dropdown.style.display === "block";
  dropdown.style.display = isVisible ? "none" : "block";


  if (!isVisible) {
    await fetchNotifications();

    // 🔁 Segna come lette sul backend
    await fetch("${BASE_API}/api-notifications/mark-as-read/", {
      method: "POST",
      headers: { Authorization: `Token ${token}` }
    });

    // 🔁 Nascondi il badge dopo la lettura
    document.getElementById("notification-badge").style.display = "none";
  }
}

// Elimina post
async function deletePost(slug) {
  const confirmDel = confirm("Vuoi eliminare questo post?");
  if (!confirmDel) return;

  await fetch(`${API_POSTS}/${slug}`, {
    method: "DELETE",
    headers: { Authorization: `Token ${token}` }
  });

  fetchAndDisplayPosts();
}



// All'avvio
(async () => {
  await loadCurrentUser();
  await fetchPosts();
  fetchNotifications();
})();
