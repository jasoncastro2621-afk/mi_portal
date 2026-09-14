document.addEventListener("DOMContentLoaded", function() {
    console.log("Portal Educativo - Jardín Escuela e Instituto Jesús Nazareno cargado correctamente.");

    // 1. RESALTAR EL ENLACE DE NAVEGACIÓN ACTIVO
    const links = document.querySelectorAll(".nav-menu a");
    const currentUrl = window.location.pathname;

    links.forEach(link => {
        const href = link.getAttribute("href");
        if (href) {
            const isHomeMatch = (currentUrl === "/" || currentUrl === "/inicio") && (href === "/" || href === "/inicio");
            const isOtherMatch = href !== "/" && href !== "/inicio" && currentUrl.includes(href);

            if (isHomeMatch || isOtherMatch) {
                link.style.color = "var(--accent-gold)";
                link.style.borderBottom = "2px solid var(--accent-gold)";
                link.style.paddingBottom = "4px";
            }
        }
    });

    // 1.1. CONTROL DEL MENÚ MÓVIL DESPLEGABLE
    const menuToggle = document.getElementById("menuToggle");
    const navMenu = document.getElementById("navMenu");

    if (menuToggle && navMenu) {
        menuToggle.addEventListener("click", function(e) {
            e.stopPropagation();
            navMenu.classList.toggle("open");
            navMenu.classList.toggle("show");
        });

        const menuLinks = navMenu.querySelectorAll("a");
        menuLinks.forEach(link => {
            link.addEventListener("click", function() {
                navMenu.classList.remove("open");
                navMenu.classList.remove("show");
            });
        });

        document.addEventListener("click", function(e) {
            if (!navMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                navMenu.classList.remove("open");
                navMenu.classList.remove("show");
            }
        });
    }

    // 2. ANIMACIÓN DE APARICIÓN AL HACER SCROLL (FADE-IN)
    const observerOptions = {
        root: null,
        rootMargin: "0px",
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visible");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll(".fade-in");
    animatedElements.forEach(el => observer.observe(el));

    // 3. ACORDEÓN INDEPENDIENTE PARA PREGUNTAS FRECUENTES (FAQ)
    const faqQuestions = document.querySelectorAll(".faq-question");

    faqQuestions.forEach(question => {
        question.addEventListener("click", function() {
            const faqItem = this.parentElement;
            const isOpen = faqItem.classList.contains("active");

            // Cierra todas las preguntas primero
            document.querySelectorAll(".faq-item").forEach(item => {
                item.classList.remove("active");
                const otherAnswer = item.querySelector(".faq-answer");
                const otherIcon = item.querySelector(".faq-icon");
                if (otherAnswer) otherAnswer.style.maxHeight = "0px";
                if (otherIcon) {
                    otherIcon.textContent = "+";
                    otherIcon.style.transform = "rotate(0deg)";
                }
            });

            // Si la que hizo clic no estaba abierta, la abrimos
            if (!isOpen) {
                faqItem.classList.add("active");
                const answer = faqItem.querySelector(".faq-answer");
                const icon = faqItem.querySelector(".faq-icon");
                if (answer) answer.style.maxHeight = answer.scrollHeight + "px";
                if (icon) {
                    icon.textContent = "×";
                    icon.style.transform = "rotate(90deg)";
                }
            }
        });
    });

    // 4. DETECCIÓN AUTOMÁTICA PARA AMPLIAR IMÁGENES
    const zoomableImages = document.querySelectorAll("img");
    zoomableImages.forEach(img => {
        if (!img.classList.contains("header-logo") && !img.closest(".whatsapp-float")) {
            img.style.cursor = "pointer";
            img.addEventListener("click", function() {
                ampliarImagen(this.src, this.alt || "Jardín Escuela e Instituto Jesús Nazareno");
            });
        }
    });

    // 4.1. DETECCIÓN Y ZOOM PARA LAS TARJETAS DE CALENDARIOS (TABLAS / TEXTO)
    const calendarioCards = document.querySelectorAll(".calendario-card, .mes-card");
    calendarioCards.forEach(card => {
        card.addEventListener("click", function(e) {
            if (e.target.tagName === 'A') return;
            
            const imgInside = this.querySelector("img");
            if (imgInside) {
                ampliarImagen(imgInside.src, imgInside.alt || "Calendario Escolar - Jesús Nazareno");
            } else {
                abrirModalCalendario(this.innerHTML);
            }
        });
    });
});

// 5. MODAL GLOBAL PARA AMPLIAR IMÁGENES
function ampliarImagen(imagenSrc, titulo) {
    let modal = document.getElementById("imageModal");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "imageModal";
        modal.style.position = "fixed";
        modal.style.top = "0";
        modal.style.left = "0";
        modal.style.width = "100%";
        modal.style.height = "100%";
        modal.style.backgroundColor = "rgba(0,0,0,0.85)";
        modal.style.zIndex = "2000";
        modal.style.display = "flex";
        modal.style.flexDirection = "column";
        modal.style.alignItems = "center";
        modal.style.justifyContent = "center";
        modal.style.cursor = "pointer";

        modal.innerHTML = `
            <div style="position: relative; max-width: 90%; max-height: 90%; text-align: center;" onclick="event.stopPropagation()">
                <img id="modalImg" src="" alt="" style="max-width: 100%; max-height: 80vh; border-radius: 8px; border: 3px solid var(--accent-gold); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <p id="modalCaption" style="color: #fff; font-size: 1.1rem; margin-top: 1rem; font-weight: 600;"></p>
                <span onclick="cerrarModalExterno()" style="position: absolute; top: -35px; right: -5px; color: #fff; font-size: 2.5rem; font-weight: bold; cursor: pointer; background: rgba(0,0,0,0.5); width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">&times;</span>
            </div>
        `;

        modal.addEventListener("click", function() {
            modal.style.display = "none";
        });

        document.body.appendChild(modal);
    }

    document.getElementById("modalImg").src = imagenSrc;
    document.getElementById("modalCaption").innerText = titulo || "Jesús Nazareno";
    modal.style.display = "flex";
}

function cerrarModalExterno() {
    let modal = document.getElementById("imageModal");
    if (modal) {
        modal.style.display = "none";
    }
}

// 6. MODAL ESPECIAL PARA CALENDARIOS EN FORMATO TEXTO/TABLA
function abrirModalCalendario(contenidoHTML) {
    let modal = document.getElementById("calendarModal");
    if (!modal) {
        modal = document.createElement("div");
        modal.id = "calendarModal";
        modal.style.position = "fixed";
        modal.style.top = "0";
        modal.style.left = "0";
        modal.style.width = "100%";
        modal.style.height = "100%";
        modal.style.backgroundColor = "rgba(0,0,0,0.85)";
        modal.style.zIndex = "2000";
        modal.style.display = "flex";
        modal.style.alignItems = "center";
        modal.style.justifyContent = "center";
        modal.style.cursor = "pointer";

        modal.innerHTML = `
            <div id="calendarModalContent" style="position: relative; background: #ffffff; padding: 2rem; border-radius: 12px; max-width: 500px; width: 90%; max-height: 90vh; overflow-y: auto; box-shadow: 0 15px 40px rgba(0,0,0,0.5);" onclick="event.stopPropagation()">
                <div id="modalBodyHtml"></div>
                <span onclick="cerrarModalCalendario()" style="position: absolute; top: 10px; right: 15px; color: #333; font-size: 2rem; font-weight: bold; cursor: pointer;">&times;</span>
            </div>
        `;

        modal.addEventListener("click", function() {
            modal.style.display = "none";
        });

        document.body.appendChild(modal);
    }

    document.getElementById("modalBodyHtml").innerHTML = contenidoHTML;
    modal.style.display = "flex";
}

function cerrarModalCalendario() {
    let modal = document.getElementById("calendarModal");
    if (modal) {
        modal.style.display = "none";
    }
}