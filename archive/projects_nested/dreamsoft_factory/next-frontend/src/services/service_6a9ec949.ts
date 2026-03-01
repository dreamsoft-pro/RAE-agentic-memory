import api from '@/lib/api';
import { defer, each } from 'lodash';

class OrderManager {
    private pageSizeSelect: any; // Replace `any` with appropriate type based on context
    private pagingSettings: any; // Replace `any` with appropriate type based on context

    constructor() {}

    async getPageSizeSelect(): Promise<any> {
        return this.pageSizeSelect;
    }

    async getPagingSettings(): Promise<any> {
        return this.pagingSettings;
    }

    async getOrders(statuses: any[], params: any): Promise<any[]> {
        try {
            const data = await api.services.dpOrderService.getMyZone(params);
            const endOfReclamationTime = await this.getReclamationSettings();
            
            each(data, order => {
                order.reclamationOnTime = compareDate(order.ended, endOfReclamationTime.date);
            });

            return data;
        } catch (error) {
            console.error('Error fetching orders:', error);
            throw error; // Re-throw the error to be handled by the caller
        }
    }

    private async getReclamationSettings(): Promise<any> {
        try {
            const settings = await api.services.dpOrderStatusService.getAll();
            return { date: new Date() }; // Replace with actual business logic or API call
        } catch (error) {
            console.error('Error fetching reclamation settings:', error);
            throw error;
        }
    }

    private compareDate(date1: string, date2: string): boolean {
        const d1 = new Date(date1);
        const d2 = new Date(date2);
        return d1 <= d2;
    }
}

export default OrderManager;

// Example usage:
const orderManager = new OrderManager();
orderManager.getOrders([], {}).then(orders => console.log('Fetched orders:', orders));