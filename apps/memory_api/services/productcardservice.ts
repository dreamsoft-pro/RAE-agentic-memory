javascript
'use strict';

import { apiGet } from '@/lib/api';
import BACKEND_ADVICE from './backend-advice.json'; // [BACKEND_ADVICE]

angular.module('digitalprint.services')
    .factory('ProductCardService', function ($q, $http, $config) {
        const ProductCardService = {};

        const resource = getResource();

        function getResource() {
            return 'productCard';
        }

        ProductCardService.get = (productID) => apiGet($http, $config.API_URL, [resource, productID].join('/'));

        ProductCardService.getXml = (productID) => {
            const def = $q.defer();
