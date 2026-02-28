import api from '@/lib/api';
import { useEffect } from 'react';

class ClipEffect {
    private el: HTMLElement;
    private props: string[];
    private mode: string;
    private show: boolean;
    private direction: string;
    private vert: boolean;
    private size: string;
    private position: string;
    private animation: {[key: string]: number};
    private wrapper?: HTMLElement;
    private animate?: HTMLElement | HTMLImageElement;
    private distance?: number;

    constructor(el: HTMLElement, mode?: 'show' | 'hide', direction?: 'vertical' | 'horizontal') {
        this.el = el;
        this.props = ["position", "top", "bottom", "left", "right", "height", "width"];
        this.mode = mode || "hide";
        this.show = this.mode === "show";
        this.direction = direction || "vertical";
        this.vert = this.direction === "vertical";
        this.size = this.vert ? "height" : "width";
        this.position = this.vert ? "top" : "left";
        this.animation = {};
    }

    private saveProps(el: HTMLElement, props: string[]) {
        // Assume an implementation of saving properties before effect
    }

    private createWrapper(el: HTMLElement) {
        const wrapperDiv = document.createElement('div');
        wrapperDiv.style.overflow = 'hidden';
        el.parentNode?.replaceChild(wrapperDiv, el);
        wrapperDiv.appendChild(el);
        return wrapperDiv;
    }

    public async applyEffect(done?: () => void) {
        this.saveProps(this.el, this.props);
        this.el.style.display = "block";

        const animateEl = (this.el.tagName === 'IMG') ? this.createWrapper(this.el) : this.el;
        
        let distance: number | undefined;

        if (animateEl instanceof HTMLElement) {
            distance = parseInt(window.getComputedStyle(animateEl)[this.size], 10);
        }

        if (this.show) {
            animateEl.style[this.size] = "0px";
            animateEl.style[this.position] = `${distance / 2}px`;
        }

        this.animation[this.size] = this.show ? distance : 0;
        this.animation[this.position] = this.show ? 0 : distance / 2;

        // Use native async/await for animation
        await new Promise((resolve) => {
            setTimeout(() => resolve(), this.show ? 500 : 1000); // Placeholder for actual animation logic
        });

        if (done) done();
    }
}

export default function ClipEffectComponent({ elRef, mode, direction }) {
    useEffect(() => {
        const clipEffect = new ClipEffect(elRef.current);
        clipEffect.applyEffect();

        return () => { /* Cleanup */ };
    }, []);

    return <div ref={elRef} />;
}