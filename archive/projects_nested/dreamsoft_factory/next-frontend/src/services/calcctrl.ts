javascript
const { resolvePromise } = require('@/lib/api');

function processCarts(carts, addressID) {
    const deferred = $q.defer();

    carts.forEach((cart, index) => {
        if (cart.ProductAddresses.length === 1 && cart.ProductAddresses[0].addressID === addressID && cart.ProductAddresses[0].join === true) {
            deferred.resolve(cart);
        }

        if (carts.length === index + 1) {
            deferred.resolve(false);
        }
    });

    return deferred.promise;
}

function addToJoinedDelivery(addressID, currency) {
    const deferred = $q.defer();
    DpOrderService.addToJoinedDelivery(addressID, currency).then(data => resolvePromise(deferred, data));
    return deferred.promise;
}
