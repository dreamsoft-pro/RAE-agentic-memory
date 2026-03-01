/**
 * Created by Rafał on 31-08-2017.
 */
angular.module('digitalprint.services')
    .service('ReclamationFaultService', function ($rootScope, $q, $http, $config) {

        var ReclamationFaultService = {};

        var resource = 'dp_reclamation_faults';

        ReclamationFaultService.getFaults = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        ReclamationFaultService.addFault = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationFaultService.removeFault = function (faultID) {

            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, faultID].join('/')
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationFaultService.editFault = function (data) {

            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource].join('/'),
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ReclamationFaultService;

    });