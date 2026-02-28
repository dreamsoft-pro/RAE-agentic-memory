import api from "@/lib/api";

class EffectManager {

    private el: HTMLElement;
    private props: string[] = ["position", "top", "bottom", "left", "right", "height", "width"];
    private mode: 'show' | 'hide';
    private show: boolean;
    private hide: boolean;
    private size: number | string;
    private percent?: RegExpMatchArray;
    private horizFirst: boolean;
    private widthFirst: boolean;
    private ref: [string, string];
    private duration: number;
    private wrapper: HTMLElement;
    private distance: [number, number];
    private animation1: Record<string, any>;
    private animation2: Record<string, any>;

    constructor(el: HTMLElement, options: { mode?: 'show' | 'hide', size?: number | string, horizFirst?: boolean, duration?: number }) {
        this.el = el;
        this.mode = options.mode || "hide";
        this.show = this.mode === "show";
        this.hide = this.mode === "hide";
        this.size = options.size || 15;
        this.horizFirst = !!options.horizFirst;
        this.widthFirst = this.show !== this.horizFirst;
        this.ref = this.widthFirst ? ["width", "height"] : ["height", "width"];
        this.duration = options.duration / 2;

        if (typeof this.size === 'string') {
            const matchResult = /\d+/.exec(this.size.replace('%', ''));
            if (matchResult) {
                this.percent = [matchResult[0], parseInt(matchResult[0], 10)];
            }
        }

        $.effects.save(el, this.props);
        el.show();
    }

    createWrapper(): HTMLElement {
        const wrapper = $.effects.createWrapper(this.el).css({ overflow: "hidden" });
        this.distance = this.widthFirst ? [wrapper.offsetWidth, wrapper.offsetHeight] : [wrapper.offsetHeight, wrapper.offsetWidth];
        
        if (this.percent) {
            const sizePercentage = parseInt(this.percent[1], 10) / 100 * this.distance[this.hide ? 0 : 1];
            if (this.show) {
                wrapper.css(this.horizFirst ? { height: '0', width: `${sizePercentage}px` } : { height: `${sizePercentage}px`, width: '0' });
            }
        }

        return wrapper;
    }
}