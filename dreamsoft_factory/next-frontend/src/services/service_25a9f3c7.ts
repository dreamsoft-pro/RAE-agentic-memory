import api from '@/lib/api';

class DeliveryService {
    private deliveryID: string;
    private courierID: string;
    private addressID: string;

    constructor(deliveryID: string, courierID: string, addressID: string) {
        this.deliveryID = deliveryID;
        this.courierID = courierID;
        this.addressID = addressID;
    }

    public async fetchParcelsPublic(): Promise<any> {
        const urlParams = `?deliveryID=${this.deliveryID}&courierID=${this.courierID}&addressID=${this.addressID}`;

        try {
            const response = await api.get(`${process.env.API_URL}deliveries/findParcelsPublic${urlParams}`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch parcels: ${error.message}`);
        }
    }

    public static async getDeliveryService(deliveryID: string, courierID: string, addressID: string): Promise<DeliveryService> {
        const service = new DeliveryService(deliveryID, courierID, addressID);
        await service.fetchParcelsPublic(); // Example usage of the method
        return service;
    }
}

export default DeliveryService;

// Usage example:
// (Assuming you have environment variables setup for API_URL)
// import { getDeliveryService } from '../path/to/DeliveryService';
//
// const deliveryID = 'some-delivery-id';
// const courierID = 'some-courier-id';
// const addressID = 'some-address-id';
//
// const service = await getDeliveryService(deliveryID, courierID, addressID);