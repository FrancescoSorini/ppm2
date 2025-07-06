API per un social media per il corso di Progettazione e Produzione Multimediale

-- DEPLOY su Railway.app --
Link: https://web-production-aa257.up.railway.app/
SCADENZA: 2 agosto 2025
Appena si accede al link, si presenta la pagina di login dove ci si può loggare (se già utenti) o registraze (nuovi utenti)
Si viene indirizzati quindi alla home page del social media, dove grazie all'interfaccia grafica si può navigare tra i profili dei vari utenti, cercare utenti e scorrere i post.
E' stato generato un superuser accessibile con le seguenti credenziali
User: fradmin
Password: frassword

Ho creato 3 app:
- users per gestire utenti e relativi profili, login e follow
- posts per creare e gestire post e relativi like e commenti
- notifications per creare e gestire le notifiche automatiche per varie situazioni (nuovi follower, like a post, commento sotto post e menzioni in post e/o commenti)

Ci si deve prima registrare (se non si è già utenti, una volta fatto si viene automaticamente loggati), con il login viene restituito il token di autenticazione.

Permessi implementati:
- IsSelfOrAdmin: solo admin o proprietario del profilo può modificarlo
- IsAuthorOrReadOnly: solo autore del post/commento può modificarlo/eliminarlo
- IsAdminUser: accesso riservato agli admin
- permissions.IsAuthenticated: protezione globale sulle risorse
Gli utenti admin sono una categoria di utenti a parte, questi possono moderare i contenuti postati eliminando/cancellando commenti e post di altri utenti.

Il client è composto da 3 pagine principali:
- index.html è la pagina di login, dove ci si può registrare (per nuovi utenti) o loggare (per utenti già registrati)
- home.html è la pagina principale che viene caricata dopo che si è effettuato il login, mostra nello header le informazioni e funzionalità per gli utenti e nel body mostra tutti i post e le relative informazioni ad essi
- profile.html è la pagina dedicata ai profili utente, nello header mostra le loro informazioni principali e nel body i post da loro creati
Si può navigare tra home e profili grazie a degli appositi bottoni.
I nomi degli utenti autori di post e commenti sono cliccabili e rimandano al rispettivo profilo.
La ricerca avviene scrivendo il nome completo e corretto di un utente (es. user1) e premendo il bottone "cerca".
La pagina profilo di un admin può rimandare al pannello admin di Django Rest Framework.

Funzionalità principali:
- operazioni CRUD per utenti e post
- seguire/smettere di seguire utenti
-  ricerca di utenti nella home, inserendo l'username (@username)
-  like/unlike sui post
-  creare/eliminare commenti
-  notificare nuovi eventi


Per l'installazione e avvio in locale:
```bash
git clone https://github.com/tuo-utente/social-media-api.git
cd social-media-api

Ho creato poi un ambiente virtuale e installato i pacchetti:
```bash
python -m venv venv
source venv\Scripts\activate
pip install -r requirements.txt

Eseguire le migrazioni e avviare il server:
```bash
python manage.py migrate
python manage.py runserver

Si può creare utente admin con il comando:
```bash
python manage.py createsuperuser

Aprire il browser in localhost:
- `http://127.0.0.1:8000/index.html` → pagina di login/registrazione
- `http://127.0.0.1:8000/home.html` → dopo il login
- `http://127.0.0.1:8000/admin/` → pannello Django Admin (solo admin)

Esempio API per loggarsi:
- nel browser, visitare `http://127.0.0.1:8000/api-users/login
- inserire nel box apposito il seguente contenuto
{
  "username": "mario",
  "password": "password123"
}

Esempio API per creare un post:
- nel browser, visitare `http://127.0.0.1:8000/api-posts/posts
- inserire nel box apposito il seguente contenuto
{
  "title": "Titolo del post",
  "content": "Contenuto del post"
}
