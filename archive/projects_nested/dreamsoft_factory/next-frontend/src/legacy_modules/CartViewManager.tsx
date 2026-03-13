/**
 * Service: CartViewManager
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { cartService } from './CartWidgetService';
import { configureProjectService } from './ConfigureProjectService';

/**
 */
export const CartViewManager: React.FC = () => {
    const [cart, setCart] = useState<any>(null);
    const [step, setStep] = useState<'items' | 'delivery' | 'payment'>('items');
    const [isLoading, setIsLoading] = useState(true);
    const [addresses, setAddresses] = useState<any[]>([]);
    const [selectedDelivery, setSelectedDelivery] = useState<number | null>(null);

    useEffect(() => {
        loadInitialData();
    }, []);

    const loadInitialData = async () => {
        setIsLoading(true);
        try {
            const [cartRes, addrRes] = await Promise.all([
                axios.get('/api/cart'),
                axios.get('/api/user/addresses')
            ]);
            setCart(cartRes.data);
            setAddresses(addrRes.data);
        } catch (error) {
            console.error("Checkout init failed", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handlePayment = async (paymentMethodId: number) => {
        try {
            const response = await axios.post('/api/order/finalize', {
                paymentId: paymentMethodId,
                deliveryId: selectedDelivery
            });
            if (response.data.paymentUrl) {
                window.location.href = response.data.paymentUrl;
            }
        } catch (error) {
            alert("Błąd płatności");
        }
    };

    const calculateTotal = () => {
        if (!cart || !cart.items) return "0,00";
        return cartService.calculateTotalPrice(cart.items);
    };

    if (isLoading) return <div>Ładowanie koszyka...</div>;

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-6">Twój Koszyk</h1>
            
            <div className="flex space-x-4 mb-8">
                <div className={`flex-1 h-2 ${step === 'items' ? 'bg-teal-500' : 'bg-gray-200'}`}></div>
                <div className={`flex-1 h-2 ${step === 'delivery' ? 'bg-teal-500' : 'bg-gray-200'}`}></div>
                <div className={`flex-1 h-2 ${step === 'payment' ? 'bg-teal-500' : 'bg-gray-200'}`}></div>
            </div>

            {step === 'items' && (
                <div className="space-y-4">
                    {/* Render Cart Items using cartService logic */}
                    <button 
                        onClick={() => setStep('delivery')}
                        className="bg-teal-600 text-white px-6 py-2 rounded-md hover:bg-teal-700"
                    >
                        Przejdź do dostawy
                    </button>
                </div>
            )}

            {step === 'delivery' && (
                <div className="space-y-4">
                    <h2 className="text-xl font-semibold">Wybierz sposób dostawy</h2>
                    {/* Delivery selection UI */}
                    <button 
                        onClick={() => setStep('payment')}
                        className="bg-teal-600 text-white px-6 py-2 rounded-md hover:bg-teal-700"
                    >
                        Przejdź do płatności
                    </button>
                </div>
            )}

            <div className="mt-8 border-t pt-4 flex justify-between items-center">
                <span className="text-lg">Suma do zapłaty:</span>
                <span className="text-3xl font-bold text-teal-700">{calculateTotal()} zł</span>
            </div>
        </div>
    );
};

export default CartViewManager;
