import { useEffect, useState } from 'react';
import api from '@/lib/api'; // Custom API client module

class PsPricelistService {
    private cache: Map<string, any>;

    constructor() {
        this.cache = new Map();
    }

    getUploadUrl(priceListID: string): string {
        return `${process.env.NEXT_PUBLIC_API_URL}/ps_priceLists/uploadIcon/${priceListID}`;
    }

    getAll(forceRefresh?: boolean): Promise<any[]> {
        const cachedData = this.cache.get('allPriceLists');
        
        if (!forceRefresh && cachedData) {
            return new Promise((resolve) => resolve(cachedData));
        }

        return api.get('/ps_priceLists')
            .then(response => {
                this.cache.set('allPriceLists', response.data);
                return response.data;
            })
            .catch(error => {
                console.error("Failed to fetch price lists:", error);
                throw new Error("Failed to fetch price lists");
            });
    }
}

export default PsPricelistService;

// Example usage in a React component
const MyComponent = () => {
    const [priceLists, setPriceLists] = useState<any[]>([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const service = new PsPricelistService();
                const data = await service.getAll();
                setPriceLists(data);
            } catch (error) {
                console.error("Failed to load price lists:", error);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            {priceLists.map(item => (
                <div key={item.id}>{item.name}</div>
            ))}
        </div>
    );
};