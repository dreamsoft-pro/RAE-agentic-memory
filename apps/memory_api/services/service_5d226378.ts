import axios from 'axios';
import { useEffect, useState } from 'next/navigation';

class CurrencyService {
    static async getCurrency(userID: string): Promise<any> {
        const response = await axios.get(`/api/currency/${userID}`);
        return response.data;
    }
}

export default function SelectCurrency({ userID }: { userID: string }) {
    const [currentCurrency, setCurrentCurrency] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                const data = await CurrencyService.getCurrency(userID);
                if (!data.response) {
                    return;
                }

                const idx = $rootScope.currencies.findIndex(currency => currency.code === data.currencyCode);
                if (idx > -1 && $rootScope.currentCurrency.code !== data.currencyCode) {
                    $rootScope.currentCurrency = $rootScope.currencies[idx];
                    if (data.currencyCode !== undefined) {
                        $cookieStore.put('currency', data.currencyCode);
                    }
                } else {
                    setCurrentCurrency(false);
                }
            } catch (error) {
                console.error("Failed to fetch currency: ", error);
                setCurrentCurrency(false);
            }
        })();
    }, [userID]);

    return null; // Render nothing or handle UI based on state
}