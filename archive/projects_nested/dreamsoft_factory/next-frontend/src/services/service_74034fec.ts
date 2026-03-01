import api from "@/lib/api";

class Slider {
    private handles: HTMLElement;
    private options: { value: number; values?: number[]; step?: number; min?: number; max?: number };
    private _animateOff: boolean;

    constructor(handles: HTMLElement, options: { value: number; values?: number[]; step?: number; min?: number; max?: number }) {
        this.handles = handles;
        this.options = options;
        this._animateOff = false;
    }

    public handleEvent(name: string): void {
        const resource = 'slider';
        let url: string;

        switch (name) {
            case "orientation":
                if (!this.handles) throw new Error('Handles are not initialized');
                this.handles.style.cssText = `bottom: ""; left: "";`;
                break;
            case "value":
                this._animateOff = true;
                this._refreshValue();
                this._change(null, 0);
                this._animateOff = false;
                break;
            case "values":
                this._animateOff = true;
                this._refreshValue();
                const valsLength: number = (this.options.values && this.options.values.length) || 0;
                for (let i = 0; i < valsLength; i++) {
                    this._change(null, i);
                }
                this._animateOff = false;
                break;
            case "step":
            case "min":
            case "max":
                this._animateOff = true;
                this._calculateNewMax();
                this._refreshValue();
                this._animateOff = false;
                break;
            case "range":
                this._animateOff = true;
                this._refresh();
                this._animateOff = false;
                break;

            default:
                throw new Error(`Unknown event: ${name}`);
        }
    }

    private _value(): number {
        const val: number = this.options.value || 0;
        return this._trimAlignValue(val);
    }

    // Placeholder methods for completeness
    private _refreshValue(): void { /* Implementation */ }
    private _change(event: any, index?: number): void { /* Implementation */ }
    private _calculateNewMax(): void { /* Implementation */ }
    private _refresh(): void { /* Implementation */ }
    private _trimAlignValue(value: number): number {
        // Implement trimming and aligning logic
        return value;
    }
}