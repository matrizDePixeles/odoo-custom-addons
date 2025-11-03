odoo.define('website_counter_animation.counter_animation', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');

    publicWidget.registry.counterAnimation = publicWidget.Widget.extend({
        selector: '.s_number',
        start: function () {
            this._animateCounter();
        },
        _animateCounter: function () {
            const el = this.el;
            const target = parseInt(el.textContent, 10);
            let count = 0;
            const duration = 2000; // 2 segundos
            
            // 💡 Nuevo: Define el número de pasos (iteraciones) deseado.
            // Usar un número fijo (ej: 100) garantiza que todos tarden 2000ms.
            const totalSteps = 100; 
            
            // 💡 Nuevo: Calcula el tiempo que dura cada paso (el intervalo).
            // Esto será el mismo para todos los contadores.
            const stepTime = Math.floor(duration / totalSteps); // 2000 / 100 = 20 ms
            
            // 💡 Nuevo: Calcula cuánto debe aumentar 'count' en cada paso.
            // Para un target de 10,000 y 100 pasos, el 'increment' es 100.
            const increment = Math.ceil(target / totalSteps); 

            const timer = setInterval(() => {
                // 1. Aumenta el contador por la cantidad calculada (`increment`)
                count += increment; 
                
                // 2. Si el contador supera el objetivo, lo fija en el objetivo y detiene.
                if (count >= target) {
                    count = target; // Asegura que el número final sea exacto
                    clearInterval(timer);
                }
                
                // 3. Actualiza el DOM
                el.textContent = count; 
            }, stepTime);
        },
    });
});