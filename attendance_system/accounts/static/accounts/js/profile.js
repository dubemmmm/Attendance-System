// profile.js
document.addEventListener('DOMContentLoaded', () => {
    const profileForm = document.getElementById('profile-form');

    profileForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const firstname = document.getElementById('firstname').value;
        const lastname = document.getElementById('lastname').value;

        // Example of an AJAX request to update the profile
        fetch('/update_profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ firstname, lastname })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Profile updated successfully');
            } else {
                alert('An error occurred while updating the profile');
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
