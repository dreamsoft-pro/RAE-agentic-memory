import api from '@/lib/api';

class MyController {
    private resource: any;
    private url: string;

    constructor(private params: any, private rootScope: any) {}

    async countOrders(): Promise<any> {
        try {
            const data = await api.service('DpOrderService').getMyZoneCount(this.params);
            return data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getDeliveries(): Promise<any[]> {
        try {
            const data = await api.service('DeliveryService').getAll();
            return data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getAddress(): Promise<any> {
        if (!this.rootScope.logged) return null;

        try {
            const data = await api.service('AddressService').getForUser();
            return data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}