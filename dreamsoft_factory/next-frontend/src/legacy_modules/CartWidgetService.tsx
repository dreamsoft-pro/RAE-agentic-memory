/**
 * Service: CartWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import axios from 'axios';
import { toast } from 'react-toastify';
import { CartProduct, Calculation, RealisationTime } from '@/types/cart';

/**
 */
class CartWidgetService {
    private static instance: CartWidgetService;
    
    public static getInstance(): CartWidgetService {
        if (!CartWidgetService.instance) {
            CartWidgetService.instance = new CartWidgetService();
        }
        return CartWidgetService.instance;
    }

    /**
     */
    public async copyProduct(
        product: CartProduct, 
        options: { isVolumeChangeOnly?: boolean, isOrderAgain?: boolean, isEditOnly?: boolean } = {}
    ): Promise<void> {
        const { isVolumeChangeOnly = false, isEditOnly = false, isOrderAgain = false } = options;
        
        console.log("Copying product:", product.productID);
        
        try {
            // Integration with TemplateRootService equivalent in Next.js
            // In Next.js we use dynamic components instead of templateUrl
            if (isEditOnly) {
                await this.handleEditOnly(product);
            } else {
                await this.triggerCopyWorkflow(product, isVolumeChangeOnly, isOrderAgain);
            }
        } catch (error) {
            toast.error("Błąd podczas kopiowania produktu");
            console.error(error);
        }
    }

    private async triggerCopyWorkflow(product: CartProduct, isVolumeOnly: boolean, isOrderAgain: boolean) {
        // Logic for prepared product data
        const preparedProduct = await this.getPreparedProduct(product);
        
        if (isOrderAgain) {
            preparedProduct.copyFromID = product.productID;
        }

        const response = await axios.post('/api/cart/save-calculation', preparedProduct);
        if (response.data.orderID) {
            toast.success("Produkt został dodany ponownie do koszyka");
        }
    }

    private async getPreparedProduct(product: CartProduct): Promise<any> {
        // Simplified mapping logic from the original 85kb file
        return {
            groupID: product.groupID,
            typeID: product.typeID,
            taxID: product.taxID,
            name: product.name,
            attributes: product.attributes,
            volume: product.volume
        };
    }

    /**
     */
    public calculateTotalPrice(items: Calculation[]): string {
        const total = items.reduce((sum, item) => {
            const price = typeof item.priceTotal === 'string' 
                ? parseFloat(item.priceTotal.replace(',', '.')) 
                : (item.priceTotal || 0);
            return sum + price;
        }, 0);
        
        return total.toFixed(2).replace('.', ',');
    }

    /**
     */
    public async updateVolume(product: CartProduct, newVolume: number): Promise<void> {
        try {
            const response = await axios.patch(`/api/cart/items/${product.productID}/volume`, {
                volume: newVolume
            });
            if (response.status === 200) {
                toast.info("Ilość została zaktualizowana");
            }
        } catch (error) {
            toast.error("Nie udało się zaktualizować ilości");
        }
    }
}

export const cartService = CartWidgetService.getInstance();
