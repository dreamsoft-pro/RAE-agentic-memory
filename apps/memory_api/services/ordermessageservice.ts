javascript
import { fetchBackendData } from '@/lib/api';

const OrderMessageService = {};

OrderMessageService.getMessages = (orderID) => {
    return fetchBackendData('GET', `dp_orders_messages/${orderID}`);
};

// [BACKEND_ADVICE] Heavy logic should be handled in the backend according to LEAN DESIGN principle
OrderMessageService.countMessages = () => {
    const def = Promise.defer();

    // Fetch count from backend
    fetchBackendData('GET', 'dp_orders_message_count')
        .then(data => def.resolve(data))
        .catch(error => def.reject(error));

    return def.promise;
};

export { OrderMessageService };
