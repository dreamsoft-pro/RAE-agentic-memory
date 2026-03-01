import api from '@/lib/api';

class SliderComponent extends HTMLElement {
    private _valueMin: number = 0;
    private _valueMax: number = 100;
    private numPages: number = 5; // Example value, can be calculated or passed as a prop
    private step: number = 1;

    constructor() {
        super();
        this.handleKeydown = this.handleKeydown.bind(this);
    }

    connectedCallback(): void {
        document.addEventListener('keydown', this.handleKeydown);
    }

    disconnectedCallback(): void {
        document.removeEventListener('keydown', this.handleKeydown);
    }

    private handleKeydown(event: KeyboardEvent): void {
        let newVal: number | undefined;

        switch (event.keyCode) {
            case 36: // $.ui.keyCode.HOME
                newVal = this._valueMin;
                break;
            case 35: // $.ui.keyCode.END
                newVal = this._valueMax;
                break;
            case 33: // $.ui.keyCode.PAGE_UP
                newVal = this._trimAlignValue(
                    this._value + (this._valueMax - this._valueMin) / this.numPages
                );
                break;
            case 34: // $.ui.keyCode.PAGE_DOWN
                newVal = this._trimAlignValue(
                    this._value - (this._valueMax - this._valueMin) / this.numPages
                );
                break;
            case 38: // $.ui.keyCode.UP
            case 39: // $.ui.keyCode.RIGHT:
                if (this._value === this._valueMax) {
                    return;
                }
                newVal = this._trimAlignValue(this._value + this.step);
                break;
            case 40: // $.ui.keyCode.DOWN
            case 37: // $.ui.keyCode.LEFT:
                if (this._value === this._valueMin) {
                    return;
                }
                newVal = this._trimAlignValue(this._value - this.step);
                break;
        }

        if (newVal !== undefined) {
            this.setValue(newVal);
        }
    }

    private setValue(value: number): void {
        // Assume there's some logic to set the value of a slider, e.g., updating state or dispatching an action.
        console.log(`Setting new value: ${value}`);
    }

    private _trimAlignValue(value: number): number {
        // Implement trimming and alignment logic here
        return Math.min(Math.max(this._valueMin, value), this._valueMax);
    }
}

customElements.define('slider-component', SliderComponent);

// Note: In a real-world scenario, you would likely use React components in Next.js rather than custom HTML elements.