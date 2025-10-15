document.addEventListener('DOMContentLoaded', () => {
    // ===== HERO SLIDER =====
    const slides = document.querySelectorAll('.hero-slider .slide');
    let currentSlide = 0;
    const slideInterval = 5000; // 5 seconds per slide

    function showSlide(index) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === index);
        });
    }

    function nextSlide() {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }

    if (slides.length > 0) {
        showSlide(currentSlide);
        setInterval(nextSlide, slideInterval);
    }

    // ===== SEARCH FORM =====
    const form = document.querySelector('.search-form');
    if (form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const city = document.querySelector('.input-city').value.trim();
            const date = document.querySelector('.input-date').value;
            const guests = document.querySelector('.input-guests').value;
            const eventType = document.querySelector('.input-event').value;
            const budget = document.querySelector('.input-budget').value;

            if (!city || !date || !guests || !eventType || !budget) {
                alert("Please fill all fields before searching!");
                return;
            }

            const resultBox = document.querySelector('.search-result');
            const message = `🔍 Searching venues in ${city} for ${guests} guests on ${date} for a ${eventType} with budget ₹${budget}...`;

            if (resultBox) {
                resultBox.textContent = message;
                resultBox.classList.add('visible');
            } else {
                alert(message);
            }
        });
    }

    // ===== FADE-IN ON SCROLL (INTERSECTION OBSERVER) =====
    const fadeElements = document.querySelectorAll('.footer, .cta, .features, .banquet-section, .testimonials-section');

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    obs.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        fadeElements.forEach(el => observer.observe(el));
    } else {
        const handleScrollFade = () => {
            fadeElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.top < window.innerHeight - 50) {
                    el.classList.add('visible');
                }
            });
        };
        window.addEventListener('scroll', handleScrollFade);
        handleScrollFade();
    }

    // ===== SMOOTH SCROLL FOR ANCHORS =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ===== COMING SOON CARD INTERACTIVE TILT =====
    const comingCard = document.querySelector('.coming-soon-card');

    if (comingCard) {
        comingCard.addEventListener('mousemove', (e) => {
            const rect = comingCard.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = ((y - centerY) / centerY) * 10; // up/down tilt
            const rotateY = ((x - centerX) / centerX) * 10; // left/right tilt

            comingCard.style.transform = `rotateX(${-rotateX}deg) rotateY(${rotateY}deg) scale(1.05)`;
        });

        comingCard.addEventListener('mouseleave', () => {
            comingCard.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
        });
    }
});
