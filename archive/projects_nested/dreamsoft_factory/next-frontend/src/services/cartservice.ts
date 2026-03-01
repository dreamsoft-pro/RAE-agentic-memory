javascript
import { ApiService } from '@/lib/api';

const CartService = {};

CartService.updateMessage = function(cartID, message) {
    const deferred = $q.defer();
    
    ApiService.patch([resource, cartID, 'cart_messages'].join('/'), { content: message })
        .then(data => {
            if (data.response) {
                deferred.resolve(data.item);
            } else {
                deferred.reject(data);
            }
        }, error => {
            deferred.reject(error);
        });

    return deferred.promise;
};

CartService.stats = function(params) {
    const deferred = $q.defer();

    ApiService.get([resource, 'stats'].join('/'), { params })
        .then(data => {
            deferred.resolve(data);
        }, error => {
            deferred.reject(error);
        });

    return deferred.promise;
};

return CartService;

// [BACKEND_ADVICE] Ensure that the backend handles the PATCH request correctly and returns the necessary data structure.
