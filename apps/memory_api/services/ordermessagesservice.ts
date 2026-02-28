javascript
import { BackendAPI } from '@/lib/api';

const resource = 'dp_orders_messages';

class OrderMessageService {
    static getMessages(orderID) {
        return new Promise((resolve, reject) => {
            BackendAPI.get([resource, 'myZone', orderID].join('/'))
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    static countMessages() {
        // [BACKEND_ADVICE] Add heavy logic for counting messages
        return new Promise((resolve, reject) => {
            BackendAPI.get([resource, 'count'].join('/'))
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }
}

export { OrderMessageService };
