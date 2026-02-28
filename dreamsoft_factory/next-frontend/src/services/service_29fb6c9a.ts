import api from "@/lib/api";

class SliderComponent {
    private options: { values: number[], range: boolean };
    private handles: any[];
    
    constructor(options: { values?: number[], range?: boolean }) {
        this.options = options;
        this.handles = [];
    }

    // Assuming these methods exist somewhere in the class
    private _trigger(eventName: string, event: Event, data: any): boolean | undefined {
        return true;  // Placeholder implementation
    }
    
    public values(index?: number): number[] | number {
        if (index === undefined) return this.options.values;
        return this.options.values[index];
    }

    private updateValue(index: number, newVal: number, event: Event): void {
        const otherVal = index === 0 ? this.options.values[1] : this.options.values[0];

        if (
            (this.options.values.length === 2 && this.options.range) &&
            ((index === 0 && newVal > otherVal) || (index === 1 && newVal < otherVal))
        ) {
            newVal = otherVal;
        }

        if (newVal !== this.values(index)) {
            const newValues = [...this.options.values];
            newValues[index] = newVal;

            // A slide can be canceled by returning false from the slide callback
            let allowed: boolean | undefined = this._trigger("slide", event, {
                handle: this.handles[index],
                value: newVal,
                values: newValues
            });
            otherVal = this.values(index ? 0 : 1);
            if (allowed !== false) {
                this.values(index, newVal); // Assuming a setter exists in the method signature
            }
        } else {
            if (newVal !== this.value()) {
                let allowed: boolean | undefined = this._trigger("slide", event, {
                    handle: this.handles[index],
                    value: newVal
                });
                if (allowed !== false) {
                    this.values(newVal);  // Assuming a setter exists in the method signature
                }
            }
        }
    }

    public value(val?: number): number | void {
        if (val === undefined) return this.options.values[0]; // Return first value for simplicity
        this.options.values = [val];
    }
}

// Example usage of the class would be here, but since it's a component class, you'd typically instantiate and use it in your Next.js pages or components.