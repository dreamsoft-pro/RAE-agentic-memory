import api from '@/lib/api';

class PsPricelistService {
    static async removePriceList(priceListID: string, resource: string[]): Promise<void> {
        try {
            const response = await api.delete(`/api/${resource.join('/')}/${priceListID}`);
            if (response.data) {
                return;
            } else {
                throw new Error('Failed to delete price list');
            }
        } catch (error) {
            throw error;
        }
    }

    static async getDevices(priceList: any): Promise<any> {
        try {
            const response = await api.get(`/api/${['ps_priceLists', priceList.ID, 'ps_priceListDevices'].join('/')}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    static async setDevices(pricelist: any, devices: any[]): Promise<void> {
        try {
            const response = await api.put(`/api/${['ps_priceLists', pricelist.ID].join('/')}/devices`, { devices });
            if (response.data) {
                return;
            } else {
                throw new Error('Failed to update price list devices');
            }
        } catch (error) {
            throw error;
        }
    }
}