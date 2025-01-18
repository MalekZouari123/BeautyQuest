// Initialize global variables
let allClinics = [];

// Create Icons for the UI
lucide.createIcons();

// Modal Management Functions
function showModal(modalId) {
    document.getElementById(modalId).style.display = 'flex';
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function switchModal(hideModalId, showModalId) {
    hideModal(hideModalId);
    showModal(showModalId);
}
// Scroll to section function
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}
function scrollToAbout(event) {
    event.preventDefault();
    document.getElementById('aboutSection').scrollIntoView({ behavior: 'smooth' });
}
// Feedback Handling
async function handleFeedback(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    console.log('Feedback data:', data);

    try {
        const response = await fetch('http://127.0.0.1:5000/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            alert('Thank you for your feedback!');
            hideModal('feedbackModal');
        } else {
            alert('Failed to submit feedback. Please try again.');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
        alert('An error occurred while submitting your feedback. Please try again.');
    }
}

// Toggle Password Visibility
function togglePassword(element) {
    const input = element.parentElement.querySelector('input');
    input.type = input.type === 'password' ? 'text' : 'password';
}

// User Authentication Functions
async function handleLogin(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData);

    try {
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        if (response.ok) {
            alert('Login successful!');
            hideModal('loginModal');
        } else {
            alert(result.message || 'Login failed. Please try again.');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

async function handleSignup(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const data = {
        username: formData.get('username'),
        password: formData.get('password'),
        confirm_password: formData.get('confirmPassword')
    };

    // Check password validation
    if (data.password !== data.confirm_password) {
        alert('Passwords do not match.');
        return;
    }
    if (data.password.length < 10 || !/[A-Z]/.test(data.password) || !/[a-z]/.test(data.password) || !/[0-9]/.test(data.password)) {
        alert('Password must be at least 10 characters long, include upper and lower case letters, and contain numbers.');
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        if (response.ok) {
            alert('Sign up successful!');
            hideModal('signupModal');
        } else {
            alert(result.message || 'Sign up failed. Please try again.');
        }
    } catch (error) {
        console.error('Signup error:', error);
        alert('An error occurred during sign-up. Please try again.');
    }
}

// Photo Upload and Recommendations with auto-scroll
async function handlePhotoUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('photo', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/api/upload_photo', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        if (response.ok) {
            // Create recommendations section if it doesn't exist
            let recommendationsSection = document.getElementById('recommendationsSection');
            if (!recommendationsSection) {
                recommendationsSection = document.createElement('section');
                recommendationsSection.id = 'recommendationsSection';
                recommendationsSection.className = 'recommendations-section';
                const mainContent = document.getElementById('mainContent');
                mainContent.insertBefore(recommendationsSection, mainContent.firstChild);
            }

            // Display recommendations and clinics
            displayRecommendations(data.recommendations);
            await fetchClinics();

            // Scroll to recommendations section
            setTimeout(() => {
                scrollToSection('recommendationsSection');
            }, 100);
        } else {
            alert(data.error || 'Failed to upload photo. Please try again.');
        }
    } catch (error) {
        console.error('Photo upload error:', error);
        alert('An error occurred while uploading the photo. Please try again.');
    }
}

// Fetch Clinics Data
async function fetchClinics() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_clinics');
        const data = await response.json();
        allClinics = data.clinics || [];
        filterClinics(); // Apply initial filtering
    } catch (error) {
        console.error('Error fetching clinics:', error);
        alert('Failed to fetch clinics. Please try again.');
    }
}

// Filter Clinics based on user input
function filterClinics() {
    const locationFilter = document.getElementById('locationFilter').value.trim();
    const ratingFilter = parseFloat(document.getElementById('ratingFilter').value.trim());

    let filteredClinics = allClinics;

    if (locationFilter) {
        filteredClinics = filteredClinics.filter(clinic =>
            clinic.location.toLowerCase().includes(locationFilter.toLowerCase())
        );
    }

    if (!isNaN(ratingFilter)) {
        filteredClinics = filteredClinics.filter(clinic => clinic.rating >= ratingFilter);
    }

    displayClinics(filteredClinics);
}
// Display Recommendations in UI with enhanced styling
function displayRecommendations(recommendations) {
    const section = document.getElementById('recommendationsSection');
    section.innerHTML = `
        <div class="recommendations-container">
            <h2>AI Surgery Recommendations</h2>
            <div class="recommendations-list">
                ${recommendations.map(rec => `
                    <div class="recommendation-item">
                        <div class="recommendation-content">
                            <i class="fas fa-check-circle"></i>
                            <p>${rec}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Display Clinics in UI
function displayClinics(clinics) {
    const clinicContainer = document.getElementById('clinicList');
    if (!clinicContainer) {
        console.error('Clinic list container not found!');
        return;
    }

    clinicContainer.innerHTML = clinics.length
        ? clinics.map(clinic => `
            <div class="clinic-item">
                <div class="clinic-details">
                    <img src="${clinic.photo_url}" alt="${clinic.name}" class="clinic-photo">
                    <div>
                        <h3>${clinic.name}</h3>
                        <p>Location: <a href="https://www.google.com/maps/search/?api=1&query=${clinic.latitude},${clinic.longitude}" target="_blank">${clinic.location}</a></p>
                        
                        <p>Rating: ${clinic.rating} ${getStars(clinic.rating)}</p>
                        
                    </div>
                </div>
                <img src="${clinic.qr_code_url}" alt="QR Code for ${clinic.name}" class="clinic-qr-code">
            </div>
        `).join('')
        : '<p class="no-clinics-message">No clinics found matching the selected criteria.</p>';
}

// Get Stars for Rating
function getStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;
    return '★'.repeat(fullStars) + '☆'.repeat(emptyStars);
}

// Map Initialization
function initMap() {
    const initialLocation = { lat: 36.8065, lng: 10.1815 };
    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: initialLocation,
    });
    new google.maps.Marker({
        position: initialLocation,
        map: map,
        title: 'Initial Location',
    });
}
// Utility Function for updating main content
function updateMainContent(element, method = 'append') {
    const mainContent = document.getElementById('mainContent');
    if (method === 'prepend') {
        mainContent.prepend(element);
    } else {
        mainContent.appendChild(element);
    }
}

// Event Listeners
document.getElementById('applyFiltersBtn').addEventListener('click', filterClinics);

// Close modal when clicking outside
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
};

// Initial setup when the window loads
window.onload = function () {
    initMap();
    fetchClinics();
};

// Show Reviews Section
function showReviewsSection() {
    document.getElementById('reviewsSection').style.display = 'block';
    document.getElementById('mainContent').style.display = 'none'; // Hide main content if needed
    document.getElementById('reviewsSection').scrollIntoView({ behavior: 'smooth' });
}

// Update the Reviews link to call the new function
document.querySelector('a[href="#reviewsSection"]').addEventListener('click', showReviewsSection);

function scrollToReviews(event) {
    event.preventDefault();
    document.getElementById('reviewsSection').scrollIntoView({ behavior: 'smooth' });
}
function scrollToServices(event) {
    event.preventDefault();
    document.getElementById('servicesSection').scrollIntoView({ behavior: 'smooth' });
}
