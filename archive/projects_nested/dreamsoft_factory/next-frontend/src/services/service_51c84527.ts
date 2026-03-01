import React from 'next/react';

class SliderComponent extends React.Component {
    private _precision(): number {
        // Assuming this method exists and returns the precision value
        return 2; // Placeholder for actual implementation
    }

    private adjustValue(value: number, options: { min?: number, max?: number, step: number }): number {
        let base = options.min !== null ? options.min : 0;
        let aboveMin = value - base;

        aboveMin = Math.round(aboveMin / options.step) * options.step;
        value = base + aboveMin;

        value = parseFloat(value.toFixed(this._precision()));

        if (options.max !== null && value > options.max) {
            return options.max;
        }
        if (options.min !== null && value < options.min) {
            return options.min;
        }

        return value;
    }

    private _stop(event: Event): void {
        if (!this.spinning) {
            return;
        }

        clearTimeout(this.timer);
        clearTimeout(this.mousewheelTimer);
        this.counter = 0;
        this.spinning = false;
        this._trigger("stop", event);
    }
}