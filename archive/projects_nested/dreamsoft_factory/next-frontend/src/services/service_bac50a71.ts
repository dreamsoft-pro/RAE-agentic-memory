import api from '@/lib/api';

class DpShipmentService {
    private resource: string = 'shipments'; // Assuming this is the endpoint for your shipments

    public async getShipments(): Promise<any[]> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            console.error(`Error fetching shipments from API: ${error}`);
            throw error; // Re-throw to handle it at a higher level if needed
        }
    }

    public async getShipmentById(id: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            console.error(`Error fetching shipment with ID ${id} from API: ${error}`);
            throw error;
        }
    }

    // Add more methods as necessary
}

export default DpShipmentService;