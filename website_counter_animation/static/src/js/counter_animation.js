odoo.define('website_counter_animation.counter_animation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.counterAnimation = publicWidget.Widget.extend({
        selector: '.s_number',
        
        // Propiedades de estado interno
        _isAnimating: false,
        targetValue: 0, // 💡 Nuevo: Almacena el valor objetivo original
        
        start: function () {
            // 💡 1. ALMACENAR EL VALOR OBJETIVO ORIGINAL
            // Se lee el valor del DOM antes de que la animación o el reseteo lo cambie.
            this.targetValue = parseInt(this.el.textContent, 10);
            
            // 💡 2. REINICIAR el DOM inmediatamente para que siempre inicie en 0
            this.el.textContent = '0'; 
            
            // Llama al start del padre
            return this._super.apply(this, arguments).then(() => {
                
                // 3. Crear el IntersectionObserver
                this.observer = new IntersectionObserver(entries => {
                    for (const entry of entries) {
                        if (entry.isIntersecting && !this._isAnimating) {
                            // Elemento ENTRA: Iniciar animación
                            this._animateCounter();
                        } else if (!entry.isIntersecting && this._isAnimating) {
                             // Elemento SALE: Reiniciar estado para la próxima vez
                             this._resetCounter();
                        }
                    }
                });
                
                // 4. Empieza a observar el elemento
                this.observer.observe(this.el);
            });
        },
        
        // 🗑️ Limpieza: Detener la observación y el timer al destruir el widget
        destroy: function () {
            if (this.observer) {
                this.observer.unobserve(this.el);
            }
            if (this.timer) {
                clearInterval(this.timer);
            }
            this._super.apply(this, arguments);
        },

        // 🔄 Método para limpiar el contador y estado
        _resetCounter: function() {
            if (this.timer) {
                clearInterval(this.timer);
            }
            this.el.textContent = '0'; // Fija el valor del DOM en 0
            this._isAnimating = false; // Permite una nueva animación al volver a entrar
        },

        _animateCounter: function () {
            this._isAnimating = true; 
            const el = this.el;
            
            // 💡 Usamos el valor ALMACENADO en la propiedad del widget
            const target = this.targetValue; 
            let count = 0;
            const duration = 2000;
            const totalSteps = 100;
            const stepTime = Math.floor(duration / totalSteps);
            const increment = Math.ceil(target / totalSteps);

            this.timer = setInterval(() => { 
                count += increment;

                if (count >= target) {
                    count = target;
                    clearInterval(this.timer);
                    this.timer = null;
                    // Mantenemos _isAnimating = true hasta que salga de la vista
                }
                el.textContent = count;
            }, stepTime);
        },
    });
});