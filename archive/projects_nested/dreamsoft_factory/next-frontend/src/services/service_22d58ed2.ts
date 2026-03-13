import api from "@/lib/api";
import { useEffect } from "react";

class EffectHandler {
    private wrapper: HTMLElement;
    private el: HTMLElement;
    private props: string[];
    private mode: string;
    private show: boolean;
    private margin: number;
    private distance: number;
    private vertical: boolean;
    private ref: string;
    private ref2: string;

    constructor(wrapper: HTMLElement, el: HTMLElement) {
        this.wrapper = wrapper;
        this.el = el;
        this.props = [];
        this.mode = "show"; // or "hide" based on requirement
        this.show = true; // toggle for showing/hiding effect
        this.margin = 10; // example value
        this.distance = 20; // example value
        this.vertical = false; // change to true if needed
    }

    public animate() {
        const animation: { [key: string]: number } = {};
        
        if (this.show) {
            animation[this.ref] = 0;
            animation[this.ref2] = this.margin + this.distance;
        } else {
            animation[this.ref] = this.distance;
            animation[this.ref2] = this.show ? this.margin : this.distance + this.margin;
        }

        // Simulate jQuery's animate method with a simple callback
        const duration = 500; // example value
        setTimeout(() => {
            if (this.mode === "hide") {
                this.el.style.display = 'none';
            }
            console.log('Animation complete');
        }, duration);

        console.log('Animating...');
    }

    private restore() {
        // Simulate effects restoration logic here
        console.log('Restoring original styles...');
    }

    public runEffect() {
        useEffect(() => {
            this.animate();
            this.restore(); // Call after animation if needed
        }, []);
    }
}

export default EffectHandler;