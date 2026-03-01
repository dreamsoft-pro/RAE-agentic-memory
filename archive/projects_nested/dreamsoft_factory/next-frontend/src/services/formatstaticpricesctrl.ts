// --- FILE: priceUtils.ts ---
export const extractPureObject = (priceObj: {[key: string]: any}): string => {
    const pureObj: {[key: string]: any} = {};
    for (const key in priceObj) {
        if (priceObj.hasOwnProperty(key) && key !== '$$hashKey') {
            pureObj[key] = priceObj[key];
        }
    }
    return JSON.stringify(pureObj);
};

// --- FILE: useSavePrice.ts ---
import { useState } from 'react';
import api from '@/lib/api';

export const useSavePrice = () => {
    const saveItem = (itemType: string, itemData: any) => {
        const item = { [itemType]: itemData[itemType], options: itemData.options };
        return api.post('/set', item);
    };

    const usePriceState = () => {
        const [price, setPrice] = useState({});
        const savePrice = (newPrice: any) => {
            saveItem('price', newPrice).then(
                () => Notification.success("Ok"),
                () => Notification.error("Error")
            );
        };
        return { price, savePrice };
    };

    const useExpenseState = () => {
        const [expense, setExpense] = useState({});
        const saveExpense = (newExpense: any) => {
            saveItem('expense', newExpense).then(
                () => Notification.success("Ok"),
                () => Notification.error("Error")
            );
        };
        return { expense, saveExpense };
    };

    return { usePriceState, useExpenseState };
};

// [BACKEND_ADVICE] This logic belongs in the PHP API.
// The above separation of concerns is a better approach for maintaining and scaling your application.