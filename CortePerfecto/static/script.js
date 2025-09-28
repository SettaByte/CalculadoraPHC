// JavaScript personalizado para la calculadora de cortes

// Función para manejar la barra flotante
function initFloatingBar() {
    const floatingBar = document.getElementById('floatingBar');
    if (!floatingBar) return;
    
    let isVisible = true;
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Mostrar/ocultar barra según dirección del scroll
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            if (isVisible) {
                floatingBar.style.transform = 'translateY(100px)';
                floatingBar.style.opacity = '0';
                isVisible = false;
            }
        } else {
            // Scrolling up
            if (!isVisible) {
                floatingBar.style.transform = 'translateY(0)';
                floatingBar.style.opacity = '1';
                isVisible = true;
            }
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Efecto de click en la barra flotante
    floatingBar.addEventListener('click', function() {
        // Scroll suave hacia arriba
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        
        // Efecto visual de click
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 150);
    });
}

// Función para verificar el código especial "67"
function checkSpecialCode() {
    const inputs = document.querySelectorAll('input[type="number"]');
    let code67Count = 0;
    
    inputs.forEach(input => {
        if (input.value === '67' || input.value === '67.0') {
            code67Count++;
        }
    });
    
    // Si hay 3 campos con "67", activar código especial
    if (code67Count >= 3) {
        showSpecialCodeMessage();
        setTimeout(() => {
            // Redirigir a enlace especial (configurable)
            const specialLink = 'https://example.com/special-page';
            window.open(specialLink, '_blank');
        }, 1500);
    }
}

// Función para mostrar mensaje de código especial
function showSpecialCodeMessage() {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.innerHTML = `
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: linear-gradient(135deg, #ff69b4, #ffb6c1);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(255, 105, 180, 0.4);
            z-index: 10000;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.2rem;
            animation: specialCodeAnimation 0.5s ease-out;
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
            <div>¡Código Especial Activado!</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                Redirigiendo en 3 segundos...
            </div>
        </div>
    `;
    
    // Agregar animación CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes specialCodeAnimation {
            0% {
                opacity: 0;
                transform: translate(-50%, -50%) scale(0.5);
            }
            100% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(notification);
    
    // Remover notificación después de 3 segundos
    setTimeout(() => {
        notification.remove();
        style.remove();
    }, 3000);
}

// Función para mejorar la experiencia de los botones
function enhanceButtons() {
    const buttons = document.querySelectorAll('button');
    
    buttons.forEach(button => {
        // Efecto de ripple al hacer click
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
                background: rgba(255, 255, 255, 0.4);
                border-radius: 50%;
                pointer-events: none;
                animation: rippleEffect 0.6s ease-out;
            `;
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });
    
    // Agregar animación de ripple
    const rippleStyle = document.createElement('style');
    rippleStyle.textContent = `
        @keyframes rippleEffect {
            0% {
                transform: scale(0);
                opacity: 1;
            }
            100% {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(rippleStyle);
}

// Función para tooltip personalizado
function initCustomTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    
    elements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.className = 'custom-tooltip';
            tooltip.style.cssText = `
                position: absolute;
                background: #ff69b4;
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                font-size: 0.9rem;
                box-shadow: 0 4px 15px rgba(255, 105, 180, 0.3);
                z-index: 1000;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.3s ease;
            `;
            
            document.body.appendChild(tooltip);
            
            // Posicionar tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => tooltip.style.opacity = '1', 10);
            
            this._tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this._tooltip) {
                this._tooltip.remove();
                this._tooltip = null;
            }
        });
    });
}

// Función para animaciones de entrada
function initAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'slideInUp 0.6s ease-out';
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.section-card').forEach(card => {
        observer.observe(card);
    });
}

// Función para validación mejorada de campos
function enhanceFormValidation() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Verificar código especial
            checkSpecialCode();
            
            // Validación visual
            if (this.value && parseFloat(this.value) > 0) {
                this.style.borderColor = '#28a745';
                this.style.backgroundColor = '#f8fff9';
            } else if (this.value === '') {
                this.style.borderColor = '#ffc0cb';
                this.style.backgroundColor = '#fef7f7';
            } else {
                this.style.borderColor = '#dc3545';
                this.style.backgroundColor = '#fff5f5';
            }
        });
        
        input.addEventListener('blur', function() {
            if (this.value && parseFloat(this.value) <= 0) {
                this.focus();
                this.select();
            }
        });
    });
}

// Función para efectos de hover mejorados
function enhanceHoverEffects() {
    const cards = document.querySelectorAll('.section-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Función principal de inicialización
function initializeEnhancements() {
    // Esperar a que el DOM esté completamente cargado
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initializeEnhancements, 500);
        });
        return;
    }
    
    try {
        initFloatingBar();
        enhanceButtons();
        initCustomTooltips();
        initAnimations();
        enhanceFormValidation();
        enhanceHoverEffects();
        
        console.log('✅ Calculadora de Cortes: Mejoras JavaScript inicializadas correctamente');
    } catch (error) {
        console.error('❌ Error inicializando mejoras JavaScript:', error);
    }
}

// Ejecutar inicialización
initializeEnhancements();

// Reinicializar en cambios de página (para Streamlit)
const streamlitObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            setTimeout(initializeEnhancements, 100);
        }
    });
});

if (document.body) {
    streamlitObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Manejar redimensionamiento de ventana
window.addEventListener('resize', function() {
    const floatingBar = document.getElementById('floatingBar');
    if (floatingBar && window.innerWidth < 768) {
        floatingBar.style.left = '10px';
        floatingBar.style.right = '10px';
        floatingBar.style.maxWidth = 'none';
    }
});
