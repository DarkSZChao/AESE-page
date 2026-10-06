/* Accessibility labels for the retained Academix controls. */
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.navbar-brand img').forEach(function (logo) {
        logo.alt = 'Imperial College London | AESE';
    });
    document.querySelectorAll('.seq-prev').forEach(function (button) {
        button.setAttribute('aria-label', 'Previous slide');
    });
    document.querySelectorAll('.seq-next').forEach(function (button) {
        button.setAttribute('aria-label', 'Next slide');
    });
    // The original navigation supports mouse hover; add click and keyboard use.
    document.querySelectorAll('.navbar-nav > .dropdown > a').forEach(function (toggle) {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.addEventListener('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            document.querySelectorAll('.navbar-nav > .dropdown').forEach(function (item) {
                item.classList.remove('open');
                item.querySelector('a').setAttribute('aria-expanded', 'false');
            });
            toggle.parentElement.classList.add('open');
            toggle.setAttribute('aria-expanded', 'true');
        });
        toggle.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                toggle.parentElement.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
                toggle.blur();
            }
        });
    });
});
