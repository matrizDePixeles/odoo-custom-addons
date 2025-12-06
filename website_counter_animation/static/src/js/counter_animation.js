odoo.define('website_counter_animation.counter_animation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.counterAnimation = publicWidget.Widget.extend({
        selector: '.s_number',
        
        // Propiedades de estado interno
        _isAnimating: false,
        targetValue: 0, 
        timer: null, // 💡 Mejor práctica: inicializar la referencia del timer
        
        start: function () {
            
            // 💡 1. ALMACENAR Y VALIDAR EL VALOR OBJETIVO ORIGINAL
            // Se lee el valor del DOM y se asegura que sea un número entero válido (o 0 por defecto).
            const initialValue = parseInt(this.el.textContent, 10);
            // CORRECCIÓN: Manejo de NaN
            this.targetValue = isNaN(initialValue) ? 0 : initialValue; 
            
            // CORRECCIÓN: Si el valor objetivo no es positivo (0 o NaN), 
            // establecemos el valor final y omitimos la lógica de animación.
            if (this.targetValue <= 0) {
                this.el.textContent = this.targetValue;
                return this._super.apply(this, arguments);
            }

            // 💡 2. REINICIAR el DOM solo si hay una animación pendiente (targetValue > 0)
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
                this.observer = null; // Limpieza explícita
            }
            // Se mantiene la limpieza del timer.
            if (this.timer) {
                clearInterval(this.timer);
                this.timer = null; // Limpieza explícita
            }
            this._super.apply(this, arguments);
        },

        // 🔄 Método para limpiar el contador y estado
        _resetCounter: function() {
            if (this.timer) {
                clearInterval(this.timer);
                // CORRECCIÓN: Establecer this.timer a null después de limpiarlo.
                this.timer = null; 
            }
            this.el.textContent = '0'; // Fija el valor del DOM en 0
            this._isAnimating = false; // Permite una nueva animación al volver a entrar
        },

        _animateCounter: function () {
            this._isAnimating = true; 
            const el = this.el;
            
            // Usamos el valor ALMACENADO que ya está validado como positivo
            const target = this.targetValue; 
            let count = 0;
            const duration = 2000;
            const totalSteps = 100;
            const stepTime = Math.floor(duration / totalSteps);
            // Esto siempre será un número válido y positivo gracias a la validación en `start`.
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
