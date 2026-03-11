import { useEffect } from 'react';
import api from '@/lib/api';

class ProgressBar {
    private element: HTMLElement | null;
    private valueDiv: HTMLElement | null;
    private options: { value: number; max: number };
    private min: number;

    constructor(elementId: string, initialOptions?: { value?: number; max?: number }) {
        this.element = document.getElementById(elementId);
        this.valueDiv = this.element?.querySelector('.value');
        this.options = {
            value: 0,
            max: 100
        };
        if (initialOptions) {
            Object.assign(this.options, initialOptions);
        }
        this.min = 0;
    }

    public destroy(): void {
        this.element?.classList.remove(
            "ui-progressbar",
            "ui-widget",
            "ui-widget-content",
            "ui-corner-all"
        );
        this.element?.removeAttribute("role");
        this.element?.removeAttribute("aria-valuemin");
        this.element?.removeAttribute("aria-valuemax");
        this.element?.removeAttribute("aria-valuenow");

        if (this.valueDiv) {
            this.valueDiv.remove();
        }
    }

    public value(newValue?: number): number | void {
        if (newValue === undefined) {
            return this.options.value;
        }

        this.options.value = this._constrainedValue(newValue);
        this._refreshValue();
    }

    private _constrainedValue(newValue: number): number {
        if (typeof newValue !== "number") {
            newValue = 0;
        }
        
        const indeterminate = newValue === false;

        return indeterminate ? false :
            Math.min(this.options.max, Math.max(this.min, newValue));
    }

    private async _refreshValue(): Promise<void> {
        // Implement any asynchronous logic here if needed.
    }

    public setOptions(options: Partial<{ value: number; max?: number }>): void {
        const value = options.value;
        delete options.value;

        Object.assign(this.options, options);
        
        if (value !== undefined) {
            this.value(value);
        }
    }
}

// Example usage in a Next.js component
function ProgressBarComponent() {
    useEffect(() => {
        const progressBar = new ProgressBar('myProgressBar', { value: 50 });
        return () => {
            progressBar.destroy();
        };
    }, []);

    // Render UI for the progress bar here

    return <div id="myProgressBar">Progress Bar</div>;
}