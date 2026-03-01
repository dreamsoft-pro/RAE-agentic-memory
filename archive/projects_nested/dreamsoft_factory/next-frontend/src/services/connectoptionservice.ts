javascript
import { BackendService } from '@/lib/api';

angular.module('digitalprint.services')
    .service('ConnectOptionService', function ($q, Restangular, $http, $config) {

        const ConnectOptionService = {};
        const resource = 'ps_connectOptions';
        const backend = new BackendService($config.API_URL);

        ConnectOptionService.getAll = async () => {
            try {
                const response = await backend.get(resource);
                return response.data;
            } catch (error) {
                throw error.response ? error.response.data : error;
            }
        };

        ConnectOptionService.add = function (item) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: item
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ConnectOptionService.update = function (item, id) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource + '/' + id,
                data: item
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ConnectOptionService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource + '/' + id
            }).success(function () {
                def.resolve();
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ConnectOptionService;
    });
