document.addEventListener('DOMContentLoaded', () => {
    // Dark Mode Toggle
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = '<i class="fas fa-moon"></i>';
    toggleButton.className = 'theme-toggle btn btn-light';
    toggleButton.setAttribute('aria-label', 'Toggle Dark Mode');
    document.body.appendChild(toggleButton);

    // Check for saved user preference
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark') {
        document.body.classList.add('dark-mode');
        toggleButton.innerHTML = '<i class="fas fa-sun"></i>';
    }

    toggleButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');

        let theme = 'light';
        if (document.body.classList.contains('dark-mode')) {
            theme = 'dark';
            toggleButton.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            toggleButton.innerHTML = '<i class="fas fa-moon"></i>';
        }

        localStorage.setItem('theme', theme);
    });

    // Smooth Scrolling for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add fade-in animation to elements as they scroll into view
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card, .section-title').forEach(el => {
        el.classList.add('fade-in-section');
        observer.observe(el);
    });
});
