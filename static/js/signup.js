// ===== ROLE TOGGLE =====
const findVenueBtn = document.getElementById('findVenueBtn');
const listVenueBtn = document.getElementById('listVenueBtn');
const ownerFields = document.getElementById('ownerFields');

// Default state = Customer
ownerFields.style.display = 'none';

findVenueBtn.addEventListener('click', () => {
    findVenueBtn.classList.add('active');
    listVenueBtn.classList.remove('active');
    ownerFields.style.display = 'none';
});

listVenueBtn.addEventListener('click', () => {
    listVenueBtn.classList.add('active');
    findVenueBtn.classList.remove('active');
    ownerFields.style.display = 'block';
});

// ===== FORM SUBMISSION =====
const form = document.getElementById('signupForm');

form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Input values
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('agreeTerms');

    // Password match check
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Terms checkbox check
    if (!terms.checked) {
        alert("Please agree to the Terms & Conditions.");
        return;
    }

    // Check current role
    const isOwner = listVenueBtn.classList.contains('active');

    // CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Collect form data
    const formData = new FormData();
    formData.append('role', isOwner ? 'owner' : 'customer');
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('email', email);
    formData.append('password1', password);
    formData.append('password2', confirmPassword);

    if (isOwner) {
        const venueName = document.getElementById('venueName').value.trim();
        const venueAddress = document.getElementById('venueAddress').value.trim();
        const venueCapacity = document.getElementById('venueCapacity').value;
        const venuePrice = document.getElementById('venuePrice').value;

        formData.append('venue_name', venueName);
        formData.append('venue_address', venueAddress);
        formData.append('venue_capacity', venueCapacity);
        formData.append('venue_price', venuePrice);
    }

    // Send POST request to Django view
    fetch("/signup/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`Signup successful as ${data.role.toUpperCase()}!`);
            form.reset();
            ownerFields.style.display = 'none';
            findVenueBtn.classList.add('active');
            listVenueBtn.classList.remove('active');
            window.location.href = "/"; // Redirect to landing page
        } else {
            let errors = '';
            for (const key in data.errors) {
                errors += `${key}: ${data.errors[key]}\n`;
            }
            alert("Error:\n" + errors);
        }
    })
    .catch(error => console.error("Error:", error));
});

// ===== SOCIAL LOGIN BUTTONS =====
const googleBtn = document.querySelector('.google-login');
const facebookBtn = document.querySelector('.facebook-login');

googleBtn.addEventListener('click', () => {
    alert("Google login clicked! Implement OAuth here.");
});

facebookBtn.addEventListener('click', () => {
    alert("Facebook login clicked! Implement OAuth here.");
});
