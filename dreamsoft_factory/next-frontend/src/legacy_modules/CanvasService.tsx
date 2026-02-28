/**
 * Service: CanvasService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import _ from 'lodash';

interface Filter {
    value: any;
    sliderValue?: number;
}

class CanvasService {
    private canvas: HTMLCanvasElement | null = null;
    private context: CanvasRenderingContext2D | null = null;
    private stage: any; // You might need to define a more specific type for the stage if you use it.
    private bitmap: ImageBitmap | null = null;
    private container: HTMLElement | null = null;
    private mask: any; // Define a more specific type for the mask if you use it.
    private filters: { [key: string]: Filter } = {};

    public setCanvas(newCanvas: HTMLCanvasElement): void {
        this.canvas = newCanvas;
    }

    public setContext(newContext: CanvasRenderingContext2D): void {
        this.context = newContext;
    }

    public getCanvas(): HTMLCanvasElement | null {
        return this.canvas;
    }

    public getContext(): CanvasRenderingContext2D | null {
        return this.context;
    }

    public setStage(newStage: any): void {
        this.stage = newStage;
    }

    public getStage(): any {
        return this.stage;
    }

    public setBitmap(newBitamp: ImageBitmap): void {
        this.bitmap = newBitamp;
    }

    public getBitmap(): ImageBitmap | null {
        return this.bitmap;
    }

    public setContainer(newContainer: HTMLElement): void {
        this.container = newContainer;
    }

    public getContainer(): HTMLElement | null {
        return this.container;
    }

    public setMask(newMask: any): void {
        this.mask = newMask;
    }

    public getMask(): any {
        return this.mask;
    }

    public setFilter(name: string, value: any, sliderValue?: number): void {
        this.filters[name] = { value, sliderValue };
    }

    public updateBitmapFilter(): void {
        if (this.bitmap) {
            this.bitmap.filters = [];
            _.each(this.filters, (one: Filter) => {
                this.bitmap.filters.push(one.value);
            });
        }
    }

    public getFilter(name: string): Filter | undefined {
        return this.filters[name];
    }

    public getFilters(): { [key: string]: Filter } {
        return this.filters;
    }
}

angular.module('digitalprint.services')
    .factory('CanvasService', function() {
        return new CanvasService();
    });