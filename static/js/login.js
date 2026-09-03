// Login page logic. Depends on the shared helpers in auth.js (isTokenValid)
// and theme.js, which must be loaded first.

// Same charset rules the backend enforces on POST /api/login — see
// FUNCTIONAL_REQUIREMENTS.md 4.6/4.7. Kept in sync with main.py's
// USERNAME_PATTERN / PASSWORD_PATTERN (no Polish diacritics allowed).
const USERNAME_PATTERN = /^[A-Za-z0-9]{1,10}$/;
const PASSWORD_PATTERN = /^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]{1,20}$/;

function showError(message) {
    const box = document.getElementById('errorBox');
    box.innerText = message;
    box.style.display = 'block';
}

function clearError() {
    const box = document.getElementById('errorBox');
    box.innerText = '';
    box.style.display = 'none';
}

// If already logged in with a valid token, skip the login screen.
if (isTokenValid()) {
    window.location.href = '/';
}

document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    clearError();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!USERNAME_PATTERN.test(username)) {
        showError('Username must be 1-10 characters: letters (no Polish characters) and digits only');
        return;
    }

    if (!PASSWORD_PATTERN.test(password)) {
        showError('Password must be 1-20 characters: letters (no Polish characters), digits and special characters only');
        return;
    }

    let res;

    try {
        res = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
    } catch (err) {
        showError('Unable to reach the server');
        return;
    }

    if (!res.ok) {
        const error = await res.json().catch(() => ({}));
        showError(error.detail || 'Invalid username or password');
        return;
    }

    const data = await res.json();

    localStorage.setItem('token', data.access_token);
    localStorage.setItem('token_expires_at', Date.now() + data.expires_in * 1000);

    window.location.href = '/';
});
