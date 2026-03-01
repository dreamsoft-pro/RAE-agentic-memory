/**
 * Created by Rafał on 08-09-2017.
 */
angular.module('digitalprint.services')
    .service('ReclamationService', function ($rootScope, $q, $http, $config) {

        var ReclamationService = {};

        var resource = 'dp_reclamations';
        var messagesResource = 'dp_reclamations_messages';

        ReclamationService.getAll = function (params) {
            var def = $q.defer();

            if (params === undefined) {
                params = {};
            }

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'myZone'].join('/'),
                params: params
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.getCount = function (params) {
            var def = $q.defer();

            if (params === undefined) {
                params = {};
            }

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'count'].join('/'),
                params: params
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.getMessages = function(reclamationID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [messagesResource, 'myZone', reclamationID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        ReclamationService.put = function (id, data) {

            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, id].join('/'),
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

        ReclamationService.create = function (data, id) {

            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'createReclamation', id].join('/'),
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

        ReclamationService.countMessages = function() {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [messagesResource, 'countAll'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.getFiles = function (reclamationID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL +  [resource, 'getFiles', reclamationID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.add = function (data, orderID) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, orderID].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.findByOrder = function (orderID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'findByOrder', orderID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        ReclamationService.getUploadUrl = function (reclamationID) {
            return $config.API_URL + [resource, 'files', reclamationID].join('/');
        };

        ReclamationService.sendEmail = function(params) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [messagesResource, 'sendEmail'].join('/'),
                data: params
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return ReclamationService;

    });