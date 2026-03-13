/**
 * Service: ConfigureProjectService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import axios from 'axios';
import _ from 'lodash';

/**
 */
export class ConfigureProjectService {
    private static instance: ConfigureProjectService;

    public static getInstance(): ConfigureProjectService {
        if (!ConfigureProjectService.instance) {
            ConfigureProjectService.instance = new ConfigureProjectService();
        }
        return ConfigureProjectService.instance;
    }

    /**
     * Updates attribute pages with validation against min/max constraints
     */
    public handlePageChange(
        currentPages: number, 
        step: number, 
        isIncrease: boolean, 
        constraints: { min?: number, max?: number } = {}
    ): number {
        let newPages = isIncrease ? currentPages + step : currentPages - step;
        
        if (constraints.min !== undefined && newPages < constraints.min) newPages = constraints.min;
        if (constraints.max !== undefined && newPages > constraints.max) newPages = constraints.max;
        if (newPages < 0) newPages = 0;

        return newPages;
    }

    /**
     * Reconstructs exclusion logic for thickness based on selected paper
     */
    public validateThickness(product: any): { isValid: boolean, error?: string } {
        const type = product.type;
        if (!type || !type.thickness) return { isValid: true };

        const currentThickness = this.calculateCurrentThickness(product);
        
        if (currentThickness < type.thickness.min) {
            return { isValid: false, error: 'thickness_too_low' };
        }
        if (currentThickness > type.thickness.max) {
            return { isValid: false, error: 'thickness_too_high' };
        }

        return { isValid: true };
    }

    private calculateCurrentThickness(product: any): number {
        // Implementation of complex thickness calculation from legacy source
        let total = 0;
        _.each(product.selectedOptions, (option) => {
            if (option.thickness) total += option.thickness;
        });
        return total;
    }

    /**
     */
    public getParamsFromUrl(searchParams: URLSearchParams): Record<string, any> {
        const params: Record<string, any> = {};
        searchParams.forEach((value, key) => {
            if (key.endsWith('[]')) {
                const cleanKey = key.slice(0, -2);
                if (!params[cleanKey]) params[cleanKey] = [];
                params[cleanKey].push(value);
            } else {
                params[key] = value;
            }
        });
        return params;
    }
}

export const configureProjectService = ConfigureProjectService.getInstance();
