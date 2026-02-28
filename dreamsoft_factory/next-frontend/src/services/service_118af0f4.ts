import axios from 'axios';
import { Ref } from 'react';

class CanvasService {
    private static bitmap: any;
    private static container: any;
    private static mask: any;
    private static filters: Record<string, { value: any; sliderValue?: number }> = {};

    public static getBitmap(): any {
        return this.bitmap;
    }

    public static setContainer(newContainer: any): void {
        this.container = newContainer;
    }

    public static getContainer(): any {
        return this.container;
    }

    public static setMask(newMask: any): void {
        this.mask = newMask;
    }

    public static getMask(): any {
        return this.mask;
    }

    public static setFilter(name: string, value: any, sliderValue?: number): void {
        this.filters[name] = { value };
        if (sliderValue !== undefined) {
            this.filters[name].sliderValue = sliderValue;
        }
    }

    public static updateBitmapFilter(): void {
        this.bitmap.filters = [];
        for (const key in this.filters) {
            if (this.filters.hasOwnProperty(key)) {
                this.bitmap.filters.push(this.filters[key].value);
            }
        }
    }
}

export default CanvasService;