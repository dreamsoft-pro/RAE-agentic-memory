import api from '@/lib/api';

class Slider {
  private options: { step?: number; max?: number };
  private resource: any;

  constructor(options: { step?: number; max?: number }) {
    this.options = options;
    this.resource = {}; // Ensure 'resource' is defined before use.
  }

  _valueMin(): number {
    return 0; // Placeholder method, adjust as needed.
  }

  _precision(): number {
    return 5; // Placeholder method, adjust as needed.
  }

  async _trimAlignValue(val: number): Promise<number> {
    if (val <= this._valueMin()) {
      return this._valueMin();
    }
    if (val >= this._valueMax()) {
      return this._valueMax();
    }
    const step = (this.options.step > 0) ? this.options.step : 1;
    const valModStep = (val - this._valueMin()) % step;
    let alignValue = val - valModStep;

    if (Math.abs(valModStep) * 2 >= step) {
      alignValue += (valModStep > 0) ? step : (-step);
    }

    return parseFloat(alignValue.toFixed(5));
  }

  async _calculateNewMax(): Promise<void> {
    const max = this.options.max;
    const min = this._valueMin();
    const step = this.options.step;
    const aboveMin = Math.floor(((max - min).toFixed(this._precision())) / step) * step;
    const newMax = aboveMin + min;

    this.max = parseFloat(newMax.toFixed(this._precision()));
  }

  private _valueMax(): number {
    return this.options.max || this._valueMin() + (this._calculateNewMax());
  }
}