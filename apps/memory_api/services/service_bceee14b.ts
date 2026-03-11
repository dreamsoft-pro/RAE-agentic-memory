import api from '@/lib/api';

class DpShipmentService {
    private resource: string = 'dp_shipment';

    public async getForOrder(orderID: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${orderID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async generateLabels(packages: any[], orderID: number): Promise<void> {
        // Implementation of the method body would go here.
        try {
            const response = await api.post(`${this.resource}/generate_labels`, { packages, orderID });
            return; // or handle success state
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default DpShipmentService;

// Example usage in a Next.js component:
import DpShipmentService from './path-to-DpShipmentService';

const myComponent = () => {
    const dpShipmentService = new DpShipmentService();

    const getOrderData = async (orderId: number) => {
        try {
            const data = await dpShipmentService.getForOrder(orderId);
            console.log(data);
        } catch (error) {
            console.error('Error fetching order shipment:', error);
        }
    };

    return (
        <div>
            {/* Your component JSX */}
        </div>
    );
};

export default myComponent;