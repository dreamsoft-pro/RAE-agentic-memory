import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getDetailPrices(optID: string, controllerID: string): Promise<any> {
        const url = `${this.resource}/${optID}/priceControllers/${controllerID}/ps_detailPrices`;
        try {
            const response = await api.get(url);
            return Restangular.stripRestangular(response.data);
        } catch (error) {
            throw error;
        }
    }

    public async setDetailPrices(optID: string, controllerID: string, prices: any): Promise<void> {
        const url = `${this.resource}/${optID}/priceControllers/${controllerID}/ps_detailPrices`;
        try {
            await api.put(url, prices);
        } catch (error) {
            throw error;
        }
    }
}