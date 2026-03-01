import api from '@/lib/api';

class PsConfigAttribute {

    private static async sort(sortList: any[]): Promise<any> {
        try {
            const response = await api.patch(`/sortAttr`, { data: sortList });
            if (response.response === true) {
                return response;
            } else {
                throw new Error('Sort operation failed');
            }
        } catch (error) {
            throw error;
        }
    }

    private static async countProducts(force?: boolean): Promise<any> {
        try {
            let cachedData = force ? undefined : cache.get('countProducts');

            if (!force && cachedData !== undefined) {
                return cachedData;

            } else {
                const response = await api.get('/ps_product_options_count');
                const data = response.data;
                cache.put('countProducts', data);
                return data;
            }
        } catch (error) {
            throw error;
        }
    }

}

// Usage example:
(async () => {
    try {
        // Call the sort method
        const sortedData = await PsConfigAttribute.sort(['attribute1', 'attribute2']);
        console.log('Sorted Data:', sortedData);

        // Call the countProducts method
        const productCount = await PsConfigAttribute.countProducts();
        console.log('Product Count:', productCount);
    } catch (error) {
        console.error('Error occurred:', error);
    }
})();