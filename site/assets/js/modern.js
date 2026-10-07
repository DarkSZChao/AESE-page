/* Shared controls; pages also remain readable without JavaScript. */
(function () {
    'use strict';
    var menuButton = document.querySelector('[data-menu-toggle]');
    var menu = document.getElementById('site-nav');
    function closeMenu() {
        if (!menuButton || !menu) return;
        menu.classList.remove('is-open');
        menuButton.setAttribute('aria-expanded', 'false');
    }
    if (menuButton && menu) {
        menuButton.addEventListener('click', function () {
            var expanded = menu.classList.toggle('is-open');
            menuButton.setAttribute('aria-expanded', String(expanded));
        });
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && menu.classList.contains('is-open')) { closeMenu(); menuButton.focus(); }
        });
        document.addEventListener('click', function (event) {
            if (!menu.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
        });
        window.matchMedia('(min-width: 961px)').addEventListener('change', closeMenu);
    }

    document.querySelectorAll('[data-carousel]').forEach(function (carousel) {
        var slides = Array.from(carousel.querySelectorAll('[data-slide]'));
        var dots = Array.from(carousel.querySelectorAll('[data-slide-to]'));
        var counter = carousel.querySelector('[data-slide-counter]');
        var pauseButton = carousel.querySelector('[data-slide-pause]');
        var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        var index = 0;
        var paused = reducedMotion.matches;
        var hovering = false;
        var timer;
        function show(nextIndex) {
            index = (nextIndex + slides.length) % slides.length;
            slides.forEach(function (slide, position) { slide.hidden = position !== index; });
            dots.forEach(function (dot, position) { dot.setAttribute('aria-pressed', String(position === index)); });
            if (counter) counter.textContent = String(index + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
        }
        function schedule() {
            window.clearInterval(timer);
            if (!paused && !hovering && !document.hidden && !carousel.contains(document.activeElement)) {
                timer = window.setInterval(function () { show(index + 1); }, 6000);
            }
        }
        carousel.querySelector('[data-slide-prev]').addEventListener('click', function () { show(index - 1); schedule(); });
        carousel.querySelector('[data-slide-next]').addEventListener('click', function () { show(index + 1); schedule(); });
        dots.forEach(function (dot) { dot.addEventListener('click', function () { show(Number(dot.dataset.slideTo)); schedule(); }); });
        function updatePause() {
            pauseButton.setAttribute('aria-pressed', String(paused));
            pauseButton.setAttribute('aria-label', paused ? 'Play slideshow' : 'Pause slideshow');
            pauseButton.textContent = paused ? '▷' : 'Ⅱ';
        }
        pauseButton.addEventListener('click', function () { paused = !paused; updatePause(); schedule(); });
        carousel.addEventListener('mouseenter', function () { hovering = true; schedule(); });
        carousel.addEventListener('mouseleave', function () { hovering = false; schedule(); });
        carousel.addEventListener('focusin', schedule);
        carousel.addEventListener('focusout', function () { window.setTimeout(schedule, 0); });
        document.addEventListener('visibilitychange', schedule);
        reducedMotion.addEventListener('change', function (event) { if (event.matches) { paused = true; updatePause(); schedule(); } });
        updatePause(); show(0); schedule();
    });

    document.querySelectorAll('[data-directory]').forEach(function (directory) {
        var cards = Array.from(directory.querySelectorAll('[data-directory-item]'));
        var buttons = Array.from(directory.querySelectorAll('[data-filter]'));
        var search = directory.querySelector('[data-search]');
        var count = directory.querySelector('[data-result-count]');
        var empty = directory.querySelector('[data-empty]');
        var category = directory.dataset.initialFilter || 'all';
        function filter() {
            var query = search ? search.value.trim().toLowerCase() : '';
            var visible = 0;
            cards.forEach(function (card) {
                var categories = (card.dataset.categories || '').split('|');
                var matches = (category === 'all' || categories.indexOf(category) !== -1) && card.textContent.toLowerCase().indexOf(query) !== -1;
                card.hidden = !matches;
                if (matches) visible += 1;
            });
            buttons.forEach(function (button) { button.setAttribute('aria-pressed', String(button.dataset.filter === category)); });
            if (count) count.textContent = visible + ' ' + (visible === 1 ? directory.dataset.singular : directory.dataset.plural);
            if (empty) empty.hidden = visible !== 0;
        }
        buttons.forEach(function (button) { button.addEventListener('click', function () { category = button.dataset.filter; filter(); }); });
        if (search) search.addEventListener('input', filter);
        filter();
    });
})();
