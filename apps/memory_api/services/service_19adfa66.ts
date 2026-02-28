import api from '@/lib/api';
import { useEffect, useState } from 'react';

type CreditLimitData = {
    deferredPayment: string;
    deferredDays: number;
    creditLimit: number;
    unpaidValue: number;
    baseCurrency: string;
};

const useCreditLimit = () => {
    const [creditLimit, setCreditLimit] = useState<CreditLimitData | boolean>(false);

    useEffect(() => {
        async function fetchCreditLimit() {
            try {
                const data: CreditLimitData = await api.get('/your-endpoint-here').then(res => res.data);
                
                if (data) {
                    data.tooltipInfo = languages.deferredPayment + '<br>'
                                       + data.deferredDays.toString() + ' ' + languages.days + '<br>'
                                       + languages.creditLimit + '<br>' 
                                       + data.creditLimit.toString() + '/' + data.unpaidValue.toString() + ' ' + data.baseCurrency;
                    setCreditLimit(data);
                } else {
                    setCreditLimit(false);
                }
            } catch (error) {
                console.error("Failed to fetch credit limit:", error);
                setCreditLimit(false);
            }
        }

        fetchCreditLimit();
    }, []);

    return { creditLimit };
};

export default useCreditLimit;