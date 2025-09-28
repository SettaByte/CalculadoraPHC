// Script para funcionalidades adicionales de la calculadora de cortes

document.addEventListener('DOMContentLoaded', function() {
    
    // Función para mejorar la experiencia del usuario
    function enhanceUserExperience() {
        
        // Agregar efectos de hover mejorados
        const buttons = document.querySelectorAll('.stButton > button');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.05)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });
        
        // Mejorar inputs numéricos
        const numberInputs = document.querySelectorAll('.stNumberInput input');
        numberInputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.style.transform = 'scale(1.02)';
                this.parentElement.style.transition = 'all 0.3s ease';
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.style.transform = 'scale(1)';
            });
        });
        
        // Agregar animaciones a las tarjetas
        const cards = document.querySelectorAll('.section-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
    
    // Función para manejar el tema
    function handleTheme() {
        const themeToggle = document.querySelector('[data-testid="stButton"]');
        if (themeToggle) {
            themeToggle.addEventListener('click', function() {
                document.body.classList.add('theme-transition');
                setTimeout(() => {
                    document.body.classList.remove('theme-transition');
                }, 300);
            });
        }
    }
    
    // Función para mejorar la barra flotante
    function enhanceFloatingBar() {
        const floatingBar = document.getElementById('floatingBar');
        if (floatingBar) {
            floatingBar.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.05) translateY(-5px)';
                this.style.boxShadow = '0 15px 40px rgba(255, 105, 180, 0.6)';
            });
            
            floatingBar.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1) translateY(0)';
                this.style.boxShadow = '0 8px 25px rgba(255, 105, 180, 0.4)';
            });
        }
    }
    
    // Función para manejar efectos de scroll
    function handleScrollEffects() {
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            const cards = document.querySelectorAll('.section-card');
            
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isVisible) {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                } else {
                    card.style.opacity = '0.7';
                    card.style.transform = 'translateY(20px)';
                }
            });
            
            lastScrollTop = scrollTop;
        });
    }
    
    // Función para agregar efectos de partículas (opcional)
    function addParticleEffect() {
        // Crear partículas flotantes sutiles
        function createParticle() {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                width: 4px;
                height: 4px;
                background: rgba(255, 105, 180, 0.3);
                border-radius: 50%;
                pointer-events: none;
                z-index: -1;
                animation: float-particle 6s linear infinite;
            `;
            
            particle.style.left = Math.random() * window.innerWidth + 'px';
            particle.style.top = window.innerHeight + 'px';
            
            document.body.appendChild(particle);
            
            setTimeout(() => {
                particle.remove();
            }, 6000);
        }
        
        // Agregar CSS para la animación de partículas
        const style = document.createElement('style');
        style.textContent = `
            @keyframes float-particle {
                to {
                    transform: translateY(-${window.innerHeight + 100}px) translateX(${Math.random() * 200 - 100}px);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Crear partículas periódicamente
        setInterval(createParticle, 2000);
    }
    
    // Función para mejorar la accesibilidad
    function enhanceAccessibility() {
        // Agregar indicadores de foco mejorados
        const focusableElements = document.querySelectorAll('button, input, [tabindex]');
        focusableElements.forEach(element => {
            element.addEventListener('focus', function() {
                this.style.outline = '3px solid #FF69B4';
                this.style.outlineOffset = '2px';
            });
            
            element.addEventListener('blur', function() {
                this.style.outline = 'none';
            });
        });
    }
    
    // Función para manejar errores de JavaScript
    function handleErrors() {
        window.addEventListener('error', function(e) {
            console.warn('Error capturado:', e.error);
            // No mostrar errores al usuario para mantener la experiencia fluida
        });
    }
    
    // Función principal para inicializar todas las mejoras
    function initialize() {
        try {
            enhanceUserExperience();
            handleTheme();
            enhanceFloatingBar();
            handleScrollEffects();
            enhanceAccessibility();
            handleErrors();
            
            // Agregar efecto de partículas solo en dispositivos con buen rendimiento
            if (window.innerWidth > 768 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                addParticleEffect();
            }
            
            console.log('✨ Mejoras de UX inicializadas correctamente');
        } catch (error) {
            console.warn('Error inicializando mejoras:', error);
        }
    }
    
    // Inicializar después de que Streamlit haya cargado completamente
    setTimeout(initialize, 1000);
    
    // Re-inicializar cuando Streamlit actualice la página
    window.addEventListener('streamlit:render', initialize);
});

// Función global para detectar múltiples easter eggs
function checkEasterEggs() {
    const inputs = document.querySelectorAll('.stNumberInput input');
    const values = Array.from(inputs).map(input => parseFloat(input.value));
    
    if (values.length === 4) {
        if (values.every(val => val === 67)) {
            console.log('🎉 Easter egg 67 activado!');
            return 'magic_67';
        } else if (values.every(val => val === 42)) {
            console.log('🌌 Easter egg 42 activado!');
            return 'answer_universe';
        } else if (JSON.stringify(values) === JSON.stringify([1, 2, 3, 4])) {
            console.log('🔢 Easter egg secuencial activado!');
            return 'sequential';
        } else if (values.every(val => val === 777)) {
            console.log('🍀 Easter egg 777 activado!');
            return 'lucky_777';
        } else if (values.every(val => val === 0)) {
            console.log('🌑 Easter egg cero activado!');
            return 'zero_void';
        } else if (values.every(val => val === 100)) {
            console.log('💯 Easter egg 100 activado!');
            return 'perfect_100';
        }
    }
    return null;
}

// Función para crear efectos visuales especiales
function createSpecialEffects() {
    // Efecto de confetti para el easter egg
    function createConfetti() {
        const colors = ['#FF69B4', '#FFB6C1', '#FFC0CB', '#FFD700', '#FFA500'];
        
        for (let i = 0; i < 50; i++) {
            setTimeout(() => {
                const confetti = document.createElement('div');
                confetti.style.cssText = `
                    position: fixed;
                    width: 10px;
                    height: 10px;
                    background: ${colors[Math.floor(Math.random() * colors.length)]};
                    top: -10px;
                    left: ${Math.random() * window.innerWidth}px;
                    border-radius: 50%;
                    pointer-events: none;
                    z-index: 9999;
                    animation: confetti-fall 3s linear forwards;
                `;
                
                document.body.appendChild(confetti);
                
                setTimeout(() => confetti.remove(), 3000);
            }, i * 50);
        }
    }
    
    // CSS para animación de confetti
    const confettiStyle = document.createElement('style');
    confettiStyle.textContent = `
        @keyframes confetti-fall {
            to {
                transform: translateY(${window.innerHeight + 100}px) rotateZ(720deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(confettiStyle);
    
    return { createConfetti };
}

// Exportar funciones globales
window.calculatorUtils = {
    checkEasterEggs,
    createSpecialEffects: createSpecialEffects()
};
