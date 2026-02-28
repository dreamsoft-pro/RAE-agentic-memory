javascript
import { BackendAdvice } from '@/lib/api';
import { defer } from 'axios';

const PaymentService = {};

PaymentService.getResource = () => {
    return ['payments', 'paymentsPublic'];
};

PaymentService.getAll = (orderID) => {
    const deferred = defer();

    const resource = this.getResource();
    resource.push(orderID);

    $http({
        method: 'GET',
        url: $config.API_URL + resource.join('/')
    }).then((response) => {
        deferred.resolve(response.data);
    }, (error) => {
        deferred.reject(error);
    });

    return deferred.promise;
};

PaymentService.getCreditLimit = () => {
    const deferred = defer();

    const resource = ['payments', 'creditLimit'];
