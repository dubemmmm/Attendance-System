// scripts.js
document.addEventListener('DOMContentLoaded', function() {
    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            if (answer.style.display === 'block') {
                answer.style.display = 'none';
                question.querySelector('.arrow').textContent = '\u25BC';
            } else {
                answer.style.display = 'block';
                question.querySelector('.arrow').textContent = '\u25B2';
            }
        });
    });
});
