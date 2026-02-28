import React, { Component } from 'react';
import api from '@/lib/api'; // Assuming this is used for any API calls in future extensions

class DropEffect extends Component {
    componentDidMount() {
        const el = document.getElementById('animated-element');
        if (!el) return;

        const mode = this.props.mode || "hide";
        let show = mode === "show";

        const direction = this.props.direction || "left";
        const ref = (direction === "up" || direction === "down") ? "top" : "left";
        
        // Setting up the initial animation properties
        const animation: {[key: string]: number} = {
            opacity: show ? 1 : 0,
            [ref]: motion(show, el)
        };

        animate(el, animation).then(() => {
            if (!show) {
                el.style.display = 'none';
            }
            this.restoreElementStyles(el);
            done();
        });
    }

    private restoreElementStyles(element: HTMLElement) {
        // Restore the element's original style properties
        Object.keys(this.props.originalStyle || {}).forEach(key => {
            element.style[key] = this.props.originalStyle[key];
        });

        if (this.props.direction === "up" || this.props.direction === "down") {
            element.style.top = '';
        } else {
            element.style.left = '';
        }
    }

    private motion(show: boolean, el: HTMLElement): number {
        const posOrNeg = show ? -1 : 1; // Determining positive or negative direction
        return (this.props.direction === "up" || this.props.direction === "left") 
                ? posOrNeg * 20 // Example distance value
                : -posOrNeg * 20;
    }

    render() {
        return <div id="animated-element"></div>;
    }
}

export default DropEffect;

// Utility function to handle animation
function animate(element: HTMLElement, properties: {[key: string]: number}): Promise<void> {
    return new Promise((resolve) => {
        // Simulating jQuery animate behavior with native JS
        const start = Date.now();
        const duration = 500; // Example duration in milliseconds

        function step() {
            if (Date.now() - start >= duration) {
                Object.keys(properties).forEach(key => element.style[key] = properties[key].toString());
                resolve();
                return;
            }

            let progress = (Date.now() - start) / duration;

            Object.keys(properties).forEach(key => {
                const value = interpolate(element, key, properties[key], progress);
                if (!isNaN(value)) element.style[key] = value + 'px'; // Adjust for CSS properties
            });

            requestAnimationFrame(step);
        }

        step();
    });
}

// Interpolation function for CSS values
function interpolate(el: HTMLElement, property: string, endValue: number, progress: number): number {
    const startValue = parseFloat(getComputedStyle(el).getPropertyValue(property));
    
    if (isNaN(startValue)) return NaN; // Fallback in case of invalid computed value

    const change = endValue - startValue;
    return startValue + change * progress;
}