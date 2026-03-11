javascript
'use strict';

const localStorageService = require('@/lib/api/localStorageService');

class OrderDataService {
    constructor(json) {
        angular.extend(this, json);
    }

    static save() {
        // [BACKEND_ADVICE] Consider backend logic for saving orders.
        localStorageService.set('orders', this.orders);
    }

    static init() {
        this.orders = localStorageService.get('orders') || [];
    }

    static setNewOrder(currency) {
        this.orders.push({ currency });
        OrderDataService.save();
    }

    static getLastOrder() {
        return this.orders.length > 0 ? this.orders[this.orders.length - 1] : {};
    }
}

// Initialize orders on module load.
OrderDataService.init();

module.exports = {
    init: OrderDataService.init,
    setNewOrder: OrderDataService.setNewOrder,
    getLastOrder: OrderDataService.getLastOrder
};
