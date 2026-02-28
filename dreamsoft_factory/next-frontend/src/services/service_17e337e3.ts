import api from '@/lib/api';

class PsPricelistService {
    async updatePriceListDevices(pricelist: any, devices: any): Promise<any> {
        const url = `${process.env.API_URL}/${['ps_priceLists', pricelist.ID, 'ps_priceListDevices'].join('/')}`;

        try {
            const response = await api.patch(url, devices);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    // Additional methods or constructor can be added here if needed
}

export default PsPricelistService;