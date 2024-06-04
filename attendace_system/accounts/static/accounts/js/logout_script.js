// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('student-login').addEventListener('click', function() {
        window.location.href = '/accounts/student-login/';
    });

    document.getElementById('teacher-login').addEventListener('click', function() {
        window.location.href = '/accounts/teacher-login/';
    });
});
