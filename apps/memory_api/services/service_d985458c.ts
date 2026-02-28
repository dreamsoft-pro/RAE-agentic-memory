import { AxiosPromise } from 'axios';
import api from '@/lib/api';

class DpShipmentService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async patchPrintLabel(shipmentID: number, orderAddressID: number): Promise<any> {
        try {
            const response = await api.patch(
                `${process.env.API_URL}/${this.resource}/printLabel`,
                { shipmentID, orderAddressID }
            );
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async deleteLabel(orderAddressID: string): Promise<any> {
        try {
            const response = await api.delete(
                `${process.env.API_URL}/${this.resource}/labels/${orderAddressID}`
            );
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}