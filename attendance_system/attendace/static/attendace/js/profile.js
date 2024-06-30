document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('profile-form');
    const editButton = document.getElementById('edit-profile-button');
    const saveButton = document.getElementById('save-profile-button');
    const cancelButton = document.getElementById('cancel-profile-button');

    const firstname = document.getElementById('firstname');
    const lastname = document.getElementById('lastname');

    let originalFirstname = firstname.value;
    let originalLastname = lastname.value;

    editButton.addEventListener('click', () => {
        firstname.removeAttribute('readonly');
        lastname.removeAttribute('readonly');

        editButton.style.display = 'none';
        saveButton.style.display = 'block';
        cancelButton.style.display = 'block';
    });

    cancelButton.addEventListener('click', () => {
        firstname.setAttribute('readonly', 'readonly');
        lastname.setAttribute('readonly', 'readonly');

        firstname.value = originalFirstname;
        lastname.value = originalLastname;

        editButton.style.display = 'block';
        saveButton.style.display = 'none';
        cancelButton.style.display = 'none';
    });

    form.addEventListener('submit', () => {
        firstname.setAttribute('readonly', 'readonly');
        lastname.setAttribute('readonly', 'readonly');

        editButton.style.display = 'block';
        saveButton.style.display = 'none';
        cancelButton.style.display = 'none';
    });
});
