javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

angular.module('digitalprint.services')
    .factory('PauseService', function($rootScope, $q, $http, $config, $cacheFactory) {

        const resource = 'pauses';
        const cache = $cacheFactory(resource);
        let getAllDef = null;

        const backendApi = new BackendApi($http, $config.API_URL);

        PauseService.getAll = function(force) {
            if (_.isNull(getAllDef) || force || (getAllDef && getAllDef.promise.$$state.status === 1)) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            backendApi.get(resource)
                .then(data => {
                    cache.put('collection', data);
                    getAllDef.resolve(data);
                })
                .catch(error => {
                    getAllDef.reject(error);
                });

            return getAllDef.promise;
        };

        PauseService.create = function(data) {
            const def = $q.defer();
