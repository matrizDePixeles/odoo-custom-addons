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
            const duration = 2000; // 2 seconds
            const stepTime = Math.abs(Math.floor(duration / target));

            const timer = setInterval(() => {
                count++;
                el.textContent = count;
                if (count >= target) {
                    clearInterval(timer);
                }
            }, stepTime);
        },
    });
});
