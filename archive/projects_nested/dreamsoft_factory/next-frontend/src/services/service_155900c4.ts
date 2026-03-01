import api from '@/lib/api';

async function fetchResource(url: string): Promise<any> {
    try {
        const response = await api.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching resource:', error);
        throw new Error('Failed to fetch resource');
    }
}

async function calculateGrossPerPcs() {
    const url = 'your-api-endpoint'; // Replace with your API endpoint
    try {
        const data = await fetchResource(url);
        
        let price = 0;
        for (let i = 0; i < data.length; i++) {
            const resource = data[i];
            
            let tmpPriceTotal = parseFloat(resource.price_total);
            if (resource.volume !== undefined) {
                tmpPriceTotal /= resource.volume;
            }
            
            price += tmpPriceTotal;
        }

        let gross_per_pcs = price.toFixed(2).replace('.', ',');
        return price.toFixed(2).replace('.', ',');
    } catch (error) {
        console.error('Error calculating gross per PCS:', error);
        throw new Error('Failed to calculate gross per PCS');
    }
}

async function changeAmount() {
    try {
        const calculatedGrossPerPcs = await calculateGrossPerPcs();
        // Use the calculated Gross_per_pcs as needed
    } catch (error) {
        console.error('Error changing amount:', error);
    }
}