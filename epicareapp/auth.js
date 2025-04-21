// Temporary user storage
let users = JSON.parse(localStorage.getItem('epicare_users')) || [];

// Register function
function register(name, email, password) {
    // Check if user already exists
    if (users.some(user => user.email === email)) {
        return { success: false, message: 'Email already registered' };
    }
    
    // Add new user
    users.push({ name, email, password });
    localStorage.setItem('epicare_users', JSON.stringify(users));
    return { success: true };
}

// Login function
function login(email, password) {
    const user = users.find(user => user.email === email && user.password === password);
    if (user) {
        // Store current session
        sessionStorage.setItem('current_user', JSON.stringify(user));
        return { success: true, user };
    }
    return { success: false, message: 'Invalid credentials' };
}

// Check if user is logged in
function checkAuth() {
    return JSON.parse(sessionStorage.getItem('current_user'));
}

// Logout function
function logout() {
    sessionStorage.removeItem('current_user');
    window.location.href = 'login.html';
}