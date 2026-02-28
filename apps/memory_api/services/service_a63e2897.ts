import api from '@/lib/api';
import $ from 'jquery';

interface ExplodeOptions {
  duration: number;
  easing?: string;
  distance?: number;
}

class EffectExplorer {

    private static animateExplode(el: JQuery, o: ExplodeOptions, done: () => void): void {
        const props = ['position', 'top', 'left'];
        let ref = 'position';
        let motion = 'both';

        $.effects.save(el, props);
        el.show();
        
        if (o.mode === "hide") {
            motion = 'reverse';
        }

        if (o.mode !== "show" && o.mode !== "hide") {
            motion = o.mode;
        }
        
        if (motion === "show") {
            ref = 'left';
        } else if (motion === "hide") {
            ref = 'right';
        }

        let pieces = Math.ceil(Math.sqrt(o.pieces)), // # of rows and columns
            position = Math.floor(pieces / 2),
            i, j,
            width = el.outerWidth(true), 
            height = el.outerHeight(true);

        $.effects.createWrapper(el).css({
            'width': width,
            'height': height
        });

        let halfWidth = width / pieces * .5;
        let halfHeight = height / pieces * .5;

        for (i = 0; i < pieces; i++) {
            for (j = (motion === "show" ? i : pieces - i - 1); j < pieces && ((i % 2) === (motion === 'hide' ? 0 : 1)); j++) {
                let thisTop = halfHeight * (pieces - i - 1 + (j % 2));
                let thisLeft = halfWidth * (i % 2 === 0 ? j : pieces - j - 1);

                el.find('div').eq(i).css({
                    width: halfWidth,
                    height: halfHeight,
                    top: thisTop - halfHeight,
                    left: thisLeft - halfWidth
                });
            }
        }

        let restore = function() {
            $.effects.restore(el, props);
            done();
        };

        el.find('div').each(function(i) {
            i = (motion === "show" ? pieces * position + i : pieces * pieces - 1 - i);

            $(this).css({
                position: 'absolute'
            }).animate({
                width: halfWidth,
                height: halfHeight,
                top: (i % pieces) * halfHeight * ((i % 2) === 0 ? 1 : -1),
                left: Math.floor(i / pieces) * halfWidth * ((i % 2) === 0 ? 1 : -1)
            }, o.duration, o.easing, function() {
                if (!--$.fx.off || !--el.data('effect-explode')) {
                    restore();
                }
            });
        });

        el.find('div').show().css({
            position: 'absolute',
            overflow: 'hidden',
            width: 0,
            height: 0,
            display: 'block'
        }).each(function(l, i) {
            $(this).animate({
                opacity: 1
            }, o.duration / 2, o.easing);
        });
    }

    public static explode(el: JQuery, options: ExplodeOptions): void {
        const defaults = {
            pieces: 16,
            duration: "fast",
            mode: "effect"
        };

        let o = $.extend({}, defaults, options),
            mode = o.mode;

        if (mode === 'show') {
            o.mode = 'hide';
        }

        el.css('position', 'relative');
        
        $(document.createElement('div'))
            .css({
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                overflow: 'hidden',
                visibility: 'visible'
            })
            .appendTo(el)
            .each(EffectExplorer.animateExplode.bind(null, el, o));

        if (mode === 'show') {
            o.mode = 'explode';
        }
    }
}