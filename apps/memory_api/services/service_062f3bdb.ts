import api from '@/lib/api';

class MyClass {
    private options: { numberFormat?: string, culture?: string, min: number, max: number };
    private element: HTMLElement;

    constructor(options: { numberFormat?: string, culture?: string, min: number, max: number }, element: HTMLElement) {
        this.options = options;
        this.element = element;
    }

    _parse(val: string): number | null {
        if (typeof val === "string" && val !== "") {
            const parsedVal = window.Globalize && this.options.numberFormat
                ? Globalize.parseFloat(val, 10, this.options.culture)
                : +val;

            return isNaN(parsedVal) || parsedVal === "" ? null : parsedVal;
        }
        return null;
    }

    _format(value: number | string): string {
        if (value === "") {
            return "";
        }
        const formattedValue = window.Globalize && this.options.numberFormat
            ? Globalize.format(value, this.options.numberFormat, this.options.culture)
            : value;

        return String(formattedValue);
    }

    _refresh(): void {
        this.element.setAttribute("aria-valuemin", this.options.min.toString());
        this.element.setAttribute("aria-valuemax", this.options.max.toString());

        const parsedVal = this._parse(this.element.value);

        if (parsedVal === null) {
            console.warn('Parsed value is null, unable to set aria-valuenow.');
            return;
        }

        this.element.setAttribute("aria-valuenow", parsedVal.toString());
    }

    isValid(): boolean {
        const value: number | string = this._parse(this.element.value);

        if (value === null) {
            return false;
        }

        const adjustedValue = this._adjustValue(value);
        return value === adjustedValue;
    }
}