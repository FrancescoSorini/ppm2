const API_USERS = "http://127.0.0.1:8000/api-users";
const API_POSTS = "http://127.0.0.1:8000/api-posts";
const token = getToken();

if (!token) window.location.href = "index.html";




// Leggi token dal cookie
function getToken() {
  const match = document.cookie.match(/(^| )token=([^;]+)/);
  return match ? match[2] : null;
}

function goHome() {
  window.location.href = "home.html";
}

// Ottieni username da query string (?user=...)
function getProfileUsername() {
  const params = new URLSearchParams(window.location.search);
  return params.get("user");
}

// Dati globali
let currentUser = null;
let profileUser = null;

// Inizializza
(async () => {
  await fetchCurrentUser();
  await fetchProfileUser();
  displayProfileInfo();
  await fetchAndDisplayPosts();
})();

// Aggiungi listener ai link follower e following
document.getElementById("follower-link").addEventListener("click", (e) => {
  e.preventDefault();
  showFollowList("followers");
});

document.getElementById("following-link").addEventListener("click", (e) => {
  e.preventDefault();
  showFollowList("following");
});

// Info utente loggato
async function fetchCurrentUser() {
  const res = await fetch(`${API_USERS}/me`, {
    headers: { Authorization: `Token ${token}` }
  });

  if (res.status === 401) return logout("Sessione scaduta");
  currentUser = await res.json();
}

// Info utente del profilo
async function fetchProfileUser() {
  const username = getProfileUsername();
  if (!username) {
    alert("Utente non specificato.");
    window.location.href = "home.html";
  }

  const res = await fetch(`${API_USERS}/search/?q=${username}`, {
    headers: { Authorization: `Token ${token}` }
  });

  const results = await res.json();
  if (!results.length) {
    alert("Utente non trovato.");
    window.location.href = "home.html";
  }

  profileUser = results[0];
}

//  Mostra info pubbliche + se owner => mostra sezione modifica
function displayProfileInfo() {

  document.getElementById("profile-username").textContent = profileUser.username;
  document.getElementById("profile-email").textContent = profileUser.email || "N/A";
  document.getElementById("profile-bio").textContent = profileUser.bio || "Nessuna bio";
  document.getElementById("profile-follower-count").textContent = profileUser.followers?.length || 0;
  document.getElementById("profile-following-count").textContent = profileUser.following?.length || 0;

  // Se owner o admin, mostra sezione modifica
  const editSection = document.getElementById("edit-profile-section");

  if (currentUser && (currentUser.id === profileUser.id || currentUser.is_staff)) {
    editSection.style.display = "block";
    document.getElementById("edit-username").value = profileUser.username;
    document.getElementById("edit-email").value = profileUser.email || "";
    document.getElementById("edit-bio").value = profileUser.bio || "";
  } else {
    editSection.style.display = "none";
  }

  // Se utente è proprietario, crea post
  if (currentUser.id === profileUser.id) {
  document.getElementById("create-post-section").style.display = "block";
  }

  // Bottone Segui/Smetti di seguire
  const followBox = document.getElementById("follow-actions");
  followBox.innerHTML = ""; // pulisci

  if (currentUser.id !== profileUser.id) {
    const isFollowing = Array.isArray(currentUser.following) &&
                        currentUser.following.includes(profileUser.id);

    const btn = document.createElement("button");
    btn.textContent = isFollowing ? "Non seguire più" : "Segui";
    btn.onclick = () => toggleFollow(profileUser.username, isFollowing);
    followBox.appendChild(btn);
  }
}

// Gestione follow/unfollow
async function toggleFollow(username, isFollowing) {
  const action = isFollowing ? "unfollow" : "follow";

  const res = await fetch(`${API_USERS}/${username}/${action}`, {
    method: "POST",
    headers: { Authorization: `Token ${token}` }
  });

  if (res.ok) {
    alert(isFollowing ? `Hai smesso di seguire @${username}.` : `Ora segui @${username}.`);
    window.location.reload(); // ricarica il profilo per aggiornare stato
  } else {
    alert("Errore nell'operazione di follow/unfollow.");
  }
}

// Lista follower e following 1
function showFollowList(listType) {
  const users = listType === 'followers' ? profileUser.followers : profileUser.following;
  const title = listType === 'followers' ? 'Follower di' : 'Seguiti da';

  if (!users || users.length === 0) {
    document.getElementById("follow-list").innerHTML = `<p>${title} @${profileUser.username}: nessuno.</p>`;
    return;
  }

  // Ricarica i dati completi dei profili con una query
  Promise.all(users.map(id => fetch(`${API_USERS}/${id}`, {
    headers: { Authorization: `Token ${token}` }
  }).then(res => res.ok ? res.json() : null)))
    .then(results => {
      const filtered = results.filter(Boolean);
      const html = `
        <h4>${title} @${profileUser.username}</h4>
        <ul>
          ${filtered.map(u => `<li><a href="profile.html?user=${u.username}">@${u.username}</a></li>`).join('')}
        </ul>
      `;
      document.getElementById("follow-list").innerHTML = html;
    });
}


// Modifica profilo
async function updateProfile() {
  const newUsername = document.getElementById("edit-username").value;
  const newEmail = document.getElementById("edit-email").value;
  const newBio = document.getElementById("edit-bio").value;

  const body = { username: newUsername, bio: newBio };
  if (newEmail) body.email = newEmail;

  const res = await fetch(`${API_USERS}/${profileUser.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`
    },
    body: JSON.stringify(body)
  });

  if (res.ok) {
    alert("Profilo aggiornato.");
    window.location.reload();
  } else {
    alert("Errore durante l'aggiornamento.");
  }
}

// Elimina account
async function deleteProfile() {
  const confirmDelete = confirm("Sei sicuro di voler eliminare l'account?");
  if (!confirmDelete) return;

  const res = await fetch(`${API_USERS}/${profileUser.id}`, {
    method: "DELETE",
    headers: { Authorization: `Token ${token}` }
  });

  if (res.ok) {
    alert("Account eliminato.");
    document.cookie = "token=; Max-Age=0; path=/";
    window.location.href = "index.html";
  } else {
    alert("Errore durante l'eliminazione.");
  }
}

// Mostra tutti i post dell'utente
async function fetchAndDisplayPosts() {
  const res = await fetch(`${API_POSTS}/posts`, {
    headers: { Authorization: `Token ${token}` }
  });

  const posts = await res.json();
  const userPosts = posts.filter(p => p.author === profileUser.username);
  const container = document.getElementById("posts-container");
  container.innerHTML = "";

  if (!userPosts.length) {
    container.innerHTML = "<p>Nessun post pubblicato.</p>";
    return;
  }

  userPosts.forEach(post => {
    const div = document.createElement("div");
    div.classList.add("post");

    div.innerHTML = `
      <h4>${post.title}</h4>
      <p>${post.content}</p>
      <small>Creato il: ${new Date(post.created_at).toLocaleString()}</small>
      <p>❤️ ${post.likes_count} like</p>

      <button onclick="likePost('${post.id}')">Mi piace</button>

      <h5>Commenti:</h5>
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
      ${(currentUser.id === profileUser.id || currentUser.is_staff) ? `
        <button onclick="deletePost('${post.id}')">Elimina post</button>
      ` : ""}
    `;

    container.appendChild(div);
  });
}

// Metti like a un post
async function likePost(slug) {
  await fetch(`${API_POSTS}/${slug}/like`, {
    method: "POST",
    headers: { Authorization: `Token ${token}` }
  });
  fetchAndDisplayPosts();
}

// Aggiungi commento
async function addComment(slug) {
  const textarea = document.getElementById(`comment-${slug}`);
  const content = textarea.value.trim();
  if (!content) return;

  await fetch(`${API_POSTS}/${slug}/comments/add`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`
    },
    body: JSON.stringify({ content })
  });

  textarea.value = "";
  fetchAndDisplayPosts();
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

// Crea post
async function createPost() {
  const title = document.getElementById("new-post-title").value.trim();
  const content = document.getElementById("new-post-content").value.trim();

  if (!title || !content) {
    alert("Inserisci sia un titolo che un contenuto.");
    return;
  }

  const res = await fetch(`${API_POSTS}/posts`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Token ${token}`
    },
    body: JSON.stringify({ title, content })
  });

  if (res.ok) {
    alert("Post pubblicato!");
    document.getElementById("new-post-title").value = "";
    document.getElementById("new-post-content").value = "";
    fetchAndDisplayPosts(); // aggiorna lista post
  } else {
    alert("Errore nella pubblicazione del post.");
  }
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
    fetchAndDisplayPosts(); // ricarica post e commenti aggiornati
  } else {
    alert("Errore durante l'eliminazione del commento.");
  }
}



// Logout
function logout(message = null) {
  document.cookie = "token=; Max-Age=0; path=/";
  if (message) alert(message);
  window.location.href = "index.html";
}
