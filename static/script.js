document.addEventListener("DOMContentLoaded", () => {
    // Navbar: sombra/opacidad extra al hacer scroll
    const navbar = document.querySelector(".navbar");
    if (navbar) {
        const toggleScrolled = () => {
            navbar.classList.toggle("scrolled", window.scrollY > 10);
        };
        toggleScrolled();
        window.addEventListener("scroll", toggleScrolled);
    }

    // Animaciones de entrada: revela elementos .reveal y .service-card
    // (fade-in + slide-up) a medida que entran en el viewport.
    const revealTargets = document.querySelectorAll(".reveal, .service-card");

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if(entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    revealTargets.forEach(target => {
        observer.observe(target);
    });

    // Smooth scrolling for menu links
    document.querySelectorAll('nav a[href^="#"]').forEach(link => {
        link.addEventListener("click", e => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute("href"));
            if(target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Menú hamburguesa (móvil/tablet)
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        const closeMenu = () => {
            navLinks.classList.remove("open");
            navToggle.classList.remove("open");
            navToggle.setAttribute("aria-expanded", "false");
        };

        navToggle.addEventListener("click", () => {
            const isOpen = navLinks.classList.toggle("open");
            navToggle.classList.toggle("open", isOpen);
            navToggle.setAttribute("aria-expanded", String(isOpen));
        });

        // Cierra el menú al elegir un enlace
        navLinks.querySelectorAll("a").forEach(link => {
            link.addEventListener("click", closeMenu);
        });

        // Cierra el menú si la pantalla vuelve a tamaño de escritorio
        window.addEventListener("resize", () => {
            if (window.innerWidth > 720) {
                closeMenu();
            }
        });
    }
});
