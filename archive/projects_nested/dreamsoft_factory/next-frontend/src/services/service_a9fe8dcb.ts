import api from '@/lib/api';
import { useEffect } from 'next/dist/client/components/app-router';
import type { FC, ReactElement } from 'react';

interface Props {
    price: any;
}

const PriceComponent: FC<Props> = ({ price }): ReactElement => {
    const [pureObj, setPureObj] = useState<any>({});

    useEffect(() => {
        const cleanPriceObject = async () => {
            const pureObj: Record<string, any> = {};
            for (const key in price) {
                if (price.hasOwnProperty(key) && key !== '$$hashKey') {
                    pureObj[key] = price[key];
                }
            }
            setPureObj(pureObj);
        };
        cleanPriceObject();
    }, [price]);

    const savePriceItem = async (item: any): Promise<void> => {
        try {
            await api.set({ price: item.price, options: item.options });
            alert('Ok');
        } catch (error) {
            console.error(error);
            alert('Error');
        }
    };

    const saveExpenseItem = async (item: any): Promise<void> => {
        try {
            await api.set({ expense: item.expense, options: item.options });
            alert('Ok');
        } catch (error) {
            console.error(error);
            alert('Error');
        }
    };

    return (
        <>
            {/* Your JSX code here */}
        </>
    );
};

export default PriceComponent;