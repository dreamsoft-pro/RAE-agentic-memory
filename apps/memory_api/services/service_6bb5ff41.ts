import { memoize } from 'lodash';

class SliderComponent {
    private _precisionOf: (num: number) => number;
    private _refreshValue: () => void;

    constructor(private options: any, private max: number) {
        this._precisionOf = memoize(this._precisionOf.bind(this));
        this._refreshValue = this._refreshValue.bind(this);
    }

    public getPrecision(): number {
        let precision = this._precisionOf(this.options.step);
        if (this.options.min !== null) {
            precision = Math.max(precision, this._precisionOf(this.options.min));
        }
        return precision;
    }

    private _precisionOf(num: number): number {
        const str = num.toString();
        const decimalIndex = str.indexOf('.');
        return decimalIndex === -1 ? 0 : str.length - decimalIndex - 1;
    }

    public getValueMin(): number | null {
        return this.options.min;
    }

    public getValueMax(): number {
        return this.max;
    }

    private _refreshValue() {
        const lastValPercent = /* placeholder for actual logic */;
        const valPercent = /* placeholder for actual logic */;
        let value = /* placeholder for actual logic */;
        const valueMin: number | null = this.options.min !== undefined ? this.options.min : null;
        const valueMax: number = this.max;

        if (this.options.range) {
            // Range handling logic
        }

        const oRange = this.options.range,
              o = this.options,
              that = this,
              animate = !this._animateOff && o.animate,
              _set = {}; // Placeholder for setting values

        // Further logic to set and update the slider value
    }
}