import api from "@/lib/api";

class ProgressBarComponent {
    private min: number;
    private max: number;
    private indeterminate: boolean;
    private element: HTMLElement;
    private valueDiv: HTMLElement;

    constructor(min: number, max: number) {
        this.min = min;
        this.max = max;
        this.indeterminate = false; // or whatever default you need
        this.element = document.createElement('div'); // Example initialization
        this.valueDiv = document.createElement('div');
    }

    private _constrainedValue(value: number): number {
        return Math.max(this.min, Math.min(this.max, value));
    }

    public setOption(key: string, value: any) {
        if (key === "max") {
            value = Math.max(this.min, value);
        }
        if (key === "disabled") {
            this.element.classList.toggle('ui-state-disabled', !!value);
            this.element.setAttribute("aria-disabled", value.toString());
        }
        // Assuming _super is a parent method, you'd call it here
    }

    private _percentage(): number {
        return this.indeterminate ? 100 : (100 * (this.options.value - this.min) / (this.max - this.min));
    }

    public refreshValue() {
        const value = this._constrainedValue(this.options.value);
        const percentage = this._percentage();

        this.valueDiv.style.display = (this.indeterminate || value > this.min) ? 'block' : 'none';
        this.valueDiv.classList.toggle('ui-corner-right', value === this.max);
        this.valueDiv.style.width = `${percentage.toFixed(0)}%`;

        this.element.classList.toggle("ui-progressbar-indeterminate", this.indeterminate);
    }
}