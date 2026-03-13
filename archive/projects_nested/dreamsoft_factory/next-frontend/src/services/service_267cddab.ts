import api from '@/lib/api';
import { useEffect, useState } from 'react';

type Product = {
    pages: Array<{ maxPages?: string; minPages?: string }>;
    getMaximumThickness: () => number;
    getMinimumThickness: () => number;
};

const useProductSelection = (product: Product) => {
    const [stopSelect, setStopSelect] = useState<NodeJS.Timeout | undefined>(undefined);

    useEffect(() => {
        if (stopSelect !== undefined) {
            clearTimeout(stopSelect);
            setStopSelect(undefined);
        }

        const timerId = setTimeout(async () => {
            let maxPages: number = product.getMaximumThickness();
            let minPages: number = product.getMinimumThickness();

            if (product.pages[0].maxPages && parseInt(product.pages[0].maxPages) > 0 && maxPages > parseInt(product.pages[0].maxPages)) {
                maxPages = parseInt(product.pages[0].maxPages);
            }

            if (product.pages[0].minPages !== null && minPages < parseInt(product.pages[0].minPages)) {
                minPages = parseInt(product.pages[0].minPages);
            }
            
            // Assuming you need to do something with maxPages and minPages, for example:
            await someFunctionThatUsesMaxAndMinPages(maxPages, minPages);

        }, 1000); // Adjust timeout as necessary

        setStopSelect(timerId);
    }, [product]);

    return { stopSelect };
};

// Example usage
const Component = ({ product }: { product: Product }) => {
    const { stopSelect } = useProductSelection(product);

    return <div>Component using product selection logic</div>;
};