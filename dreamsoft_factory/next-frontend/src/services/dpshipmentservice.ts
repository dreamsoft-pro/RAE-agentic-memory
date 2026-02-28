javascript
import { createApi } from '@/lib/api';

const DpShipmentService = {};

const resource = 'dp_shipment';

DpShipmentService.getForOrder = (orderID) => {
    return createApi().get(`${resource}/${orderID}`).then(
        (response) => response.data,
        (error) => Promise.reject(error)
    );
};

// [BACKEND_ADVICE] Heavy logic in the backend for generateLabels
DpShipmentService.generateLabels = (packages, orderID) => {
    return new Promise((resolve, reject) => {
        const data = { packages, orderID };
        
        createApi().post(`${resource}/labels`, data)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

export default DpShipmentService;
