document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.carousel-slide');
    if (slides.length === 0) return; // Exit if not on the homepage

    let currentSlide = 0;
    let autoPlayInterval;
    const intervalTime = 5000; // 5 seconds

    const allTabs = Array.from(document.querySelectorAll('.carousel-tab'));

    function showSlide(index) {
        // Hide all slides
        slides.forEach((slide, i) => {
            if (i === index) {
                slide.classList.remove('opacity-0', 'pointer-events-none');
                slide.classList.add('opacity-100');
            } else {
                slide.classList.remove('opacity-100');
                slide.classList.add('opacity-0', 'pointer-events-none');
            }
        });

        // Update navigation tabs
        allTabs.forEach((tab, i) => {
            if (i === index) {
                tab.className = 'carousel-tab flex-shrink-0 whitespace-nowrap text-base font-bold transition-all duration-300';
                tab.style.color = 'var(--md-primary-fg-color)';
            } else {
                tab.className = 'carousel-tab flex-shrink-0 whitespace-nowrap text-base font-normal text-slate-500 hover:text-slate-700 translate-y-0.5 transition-all duration-300';
                tab.style.color = '';
            }
        });

        // Center the active tab in the scrolling container
        // Since the container might have a scrolling offset, we use offsetLeft
        // offsetLeft is relative to the offsetParent (which might not be the container if relative positioning isn't set)
        // Wait, navContainer has relative positioning ('relative' class).
        const navContainer = document.getElementById('carousel-nav-container');
        const activeTab = allTabs[index];
        if (navContainer && activeTab) {
            const containerCenter = navContainer.clientWidth / 2;
            const tabCenter = activeTab.offsetLeft + (activeTab.clientWidth / 2);
            navContainer.scrollTo({
                left: tabCenter - containerCenter,
                behavior: 'smooth'
            });
        }

        currentSlide = index;
    }

    // Initialize first slide perfectly on load
    showSlide(0);

    function nextSlide() {
        showSlide((currentSlide + 1) % slides.length);
    }

    function prevSlide() {
        showSlide((currentSlide - 1 + slides.length) % slides.length);
    }

    function startAutoPlay() {
        autoPlayInterval = setInterval(nextSlide, intervalTime);
    }

    function resetAutoPlay() {
        clearInterval(autoPlayInterval);
        startAutoPlay();
    }

    // Add click listeners to tabs
    allTabs.forEach((tab, i) => {
        tab.addEventListener('click', () => {
            showSlide(i);
            resetAutoPlay();
        });
    });

    // Start autoplay
    startAutoPlay();
    // Marquee duplication logic
    const marqueeContent = document.getElementById("marquee-content");
    const marqueeContainer = document.getElementById("marquee-container");
    if (marqueeContent && marqueeContainer) {
        const clone = marqueeContent.cloneNode(true);
        clone.setAttribute("aria-hidden", "true");
        marqueeContainer.appendChild(clone);
    }
});
