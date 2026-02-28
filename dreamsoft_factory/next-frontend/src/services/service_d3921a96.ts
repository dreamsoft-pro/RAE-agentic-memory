import api from '@/lib/api';
import $ from 'jquery';  // Assuming jQuery is still used in your project

class ElementEffect {
    private el: JQuery;
    private props: string[];
    private mode: string;
    private show: boolean;
    private direction: string;
    private ref: string;
    private positiveMotion: boolean;
    private distance: number | null;
    private animation: {[key: string]: any};

    constructor(el: JQuery, options: { mode?: 'show' | 'hide', direction?: string }) {
        this.el = el;
        this.props = [ "position", "top", "bottom", "left", "right", "width", "height" ];
        this.mode = $.effects.setMode(this.el, options.mode || "show");
        this.show = this.mode === "show";
        this.direction = options.direction || "left";
        this.ref = (this.direction === "up" || this.direction === "down") ? "top" : "left";
        this.positiveMotion = (this.direction === "up" || this.direction === "left");
        this.distance = null;
        this.animation = {};

        // Adjust
        $.effects.save(this.el, this.props);
        this.el.show();
        this.distance = options.distance || el[this.ref === "top" ? "outerHeight" : "outerWidth"](true);

        $.effects.createWrapper(this.el).css({
            overflow: "hidden"
        });

        if (this.show) {
            this.el.css(this.ref, this.positiveMotion ? (isNaN(Number(this.distance)) ? "-" + this.distance : -Number(this.distance)) : this.distance);
        }

        // Animation
        this.animation[this.ref] = (this.show ?
            (this.positiveMotion ? "+=" : "-=") :
            (this.positiveMotion ? "-=" : "+=")) +
            this.distance;
    }
}