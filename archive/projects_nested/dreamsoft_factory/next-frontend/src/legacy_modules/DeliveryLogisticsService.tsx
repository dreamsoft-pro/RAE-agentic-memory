/**
 * Service: DeliveryLogisticsService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import _ from 'lodash';

export interface DeliveryMethod {
    ID: number;
    name: string;
    hasParcelShops: boolean;
    price: {
        weight: number;
        UnitQty: number;
        price: number;
        priceGross: number;
        FS_WeightStart?: number;
        FS_WeightEnd?: number;
        FS_ValStart?: number;
        FS_ValEnd?: number;
        EX_WeightStart?: number;
        EX_WeightEnd?: number;
    };
}

export interface PackageResult {
    packageCount: number;
    totalWeight: number;
    totalPriceNet: number;
    totalPriceGross: number;
    isFreeShipping: boolean;
}

/**
 */
export class DeliveryLogisticsService {
    private static instance: DeliveryLogisticsService;

    public static getInstance(): DeliveryLogisticsService {
        if (!DeliveryLogisticsService.instance) {
            DeliveryLogisticsService.instance = new DeliveryLogisticsService();
        }
        return DeliveryLogisticsService.instance;
    }

    /**
     */
    public calculateShipping(
        delivery: DeliveryMethod, 
        totalProductWeight: number, 
        orderValueNet: number,
        course: number = 1
    ): PackageResult {
        const maxWeightPerPkg = delivery.price.weight || 30;
        const maxQtyPerPkg = delivery.price.UnitQty || 1000000;

        // 1. Determine package count
        const packageCount = Math.ceil(Math.max(
            totalProductWeight / maxWeightPerPkg,
            1 // At least one package
        ));

        // 2. Check for Free Shipping rules
        const isFreeByWeight = this.checkRange(totalProductWeight, delivery.price.FS_WeightStart, delivery.price.FS_WeightEnd);
        const isFreeByValue = this.checkRange(orderValueNet * course, delivery.price.FS_ValStart, delivery.price.FS_ValEnd);
        
        const isFreeShipping = isFreeByWeight || isFreeByValue;

        // 3. Final prices
        const unitPriceNet = isFreeShipping ? 0 : delivery.price.price;
        const unitPriceGross = isFreeShipping ? 0 : delivery.price.priceGross;

        return {
            packageCount,
            totalWeight: totalProductWeight,
            totalPriceNet: packageCount * unitPriceNet,
            totalPriceGross: packageCount * unitPriceGross,
            isFreeShipping
        };
    }

    private checkRange(value: number, start?: number, end?: number): boolean {
        if (start === undefined || end === undefined || start === null || end === null) return false;
        if (start === 0 && end === 0) return false;
        return value >= start && value <= end;
    }

    /**
     */
    public filterDeliveries(methods: DeliveryMethod[], products: any[]): DeliveryMethod[] {
        const excludedIds = _.flatMap(products, p => p.excludeDeliveries || []);
        return methods.filter(m => !excludedIds.includes(m.ID));
    }
}

export const deliveryService = DeliveryLogisticsService.getInstance();
