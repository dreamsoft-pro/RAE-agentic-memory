javascript
'use strict';

import { createBackendApi } from '@/lib/api';
const backend = createBackendApi();

angular.module('digitalprint.services')
    .factory('InvoiceService', function ($q, $http, $config) {

        const InvoiceService = {};

        // [BACKEND_ADVICE] Consider moving resource retrieval to a centralized service.
        const getResource = () => 'dp_invoices';

        InvoiceService.getForUser = async (orderID) => {
            try {
                const response = await backend.get(`${getResource()}/getForUser/${orderID}`, { responseType: 'arraybuffer', dataType: 'blob' });
                return $q.resolve(response.data);
            } catch (error) {
                return $q.reject(error);
            }
        };

        return InvoiceService;
    });
