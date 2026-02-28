javascript
import { ApiService } from '@/lib/api';

const DeliveryService = {};

DeliveryService.getResource = () => ['deliveries', 'deliveriesPublic'].join('/');

DeliveryService.getAll = (currencyCode) => {
    return new Promise((resolve, reject) => {
        const resource = DeliveryService.getResource();
        ApiService.get(`${resource}/${encodeURIComponent(currencyCode)}`)
            .then(response => resolve(response.data))
            .catch(error => reject(error));
    });
};

DeliveryService.findParcelShops = (addressID, deliveryID, courierID) => {
    // [BACKEND_ADVICE] Add heavy logic here
    return new Promise((resolve, reject) => {
        const resource = DeliveryService.getResource();
