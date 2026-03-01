import api from "@/lib/api";

class Slider {
    private handles: any[];
    private options: { values?: boolean[] };
    private valueFn: () => number;
    private valuesFn: (index?: number) => number[];

    constructor(handles: any[], options: { values?: boolean[] }, valueFn: () => number, valuesFn: (index?: number) => number[]) {
        this.handles = handles;
        this.options = options;
        this.valueFn = valueFn;
        this.valuesFn = valuesFn;
    }

    private _trigger(eventName: string, event: any, uiHash: { handle: any; value: number; values?: number[] }) {
        // Placeholder for trigger logic
    }

    private _trimAlignValue(newValue: number): number {
        return newValue; // Stub method for demonstration purposes
    }

    private _refreshValue() {
        // Stub method for demonstration purposes
    }

    private _value(): number {
        return this.valueFn();
    }

    public stop(event: any, index: number) {
        let uiHash = {
            handle: this.handles[index],
            value: this._value()
        };
        if (this.options.values && this.options.values.length) {
            uiHash.value = this.valuesFn(index);
            uiHash.values = this.valuesFn();
        }
        
        this._trigger("stop", event, uiHash);
    }

    public _change(event: any, index: number) {
        if (!this._keySliding && !this._mouseSliding) {
            let uiHash = {
                handle: this.handles[index],
                value: this._value()
            };
            if (this.options.values && this.options.values.length) {
                uiHash.value = this.valuesFn(index);
                uiHash.values = this.valuesFn();
            }

            this._lastChangedValue = index;
            
            this._trigger("change", event, uiHash);
        }
    }

    public value(newValue?: number): number | void {
        if (newValue !== undefined) {
            this.options.value = this._trimAlignValue(newValue);
            this._refreshValue();
            this._change(null, 0);
            return;
        }

        return this._value();
    }
}