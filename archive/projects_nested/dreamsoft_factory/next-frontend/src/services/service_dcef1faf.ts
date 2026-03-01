import api from '@/lib/api';

class EffectHandler {
    private el: any;
    private o: any;
    private mode: string;
    private scale: string;
    private zero: { width: number; height: number };
    private original: { width: number; height: number };
    private vProps: string[];

    constructor(el: any, o: any, mode: string, scale: string, zero: { width: number; height: number }, original: { width: number; height: number }, vProps: string[]) {
        this.el = el;
        this.o = o;
        this.mode = mode;
        this.scale = scale;
        this.zero = zero;
        this.original = original;
        this.vProps = vProps;

        if (this.isToggleMode() && this.mode === "show") {
            this.el.from = { width: this.o.to?.width || this.zero.width, height: this.o.to?.height || this.zero.height };
            this.el.to = { width: this.o.from?.width || this.original.width, height: this.o.from?.height || this.original.height };
        } else {
            this.el.from = { width: this.o.from?.width || (this.mode === "show" ? this.zero.width : this.original.width), height: this.o.from?.height || (this.mode === "show" ? this.zero.height : this.original.height) };
            this.el.to = { width: this.o.to?.width || (this.mode === "hide" ? this.zero.width : this.original.width), height: this.o.to?.height || (this.mode === "hide" ? this.zero.height : this.original.height) };
        }

        // Set scaling factor
        const factor = {
            from: {
                y: this.el.from.height / this.original.height,
                x: this.el.from.width / this.original.width
            },
            to: {
                y: this.el.to.height / this.original.height,
                x: this.el.to.width / this.original.width
            }
        };

        // Scale the css box
        if (this.scale === "box" || this.scale === "both") {

            // Vertical props scaling
            if (factor.from.y !== factor.to.y) {
                const props = ["verticalProp1", "verticalProp2"]; // Example properties array
                this.el.from = $.effects.setTransition(this.el, this.vProps.concat(props), factor.from.y, this.el.from);
                this.el.to = $.effects.setTransition(this.el, this.vProps.concat(props), factor.to.y, this.el.to);
            }
        }
    }

    private isToggleMode(): boolean {
        return 'mode' in this.o && this.o.mode === "toggle";
    }
}

// Usage
const effectHandler = new EffectHandler(el, o, mode, scale, zero, original, vProps);