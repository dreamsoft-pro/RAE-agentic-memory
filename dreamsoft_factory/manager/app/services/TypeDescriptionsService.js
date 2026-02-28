'use strict';

angular.module('digitalprint.services')
    .factory('TypeDescriptionsService', function ($q, $http, $config, Restangular, FileUploader) {

        var TypeDescriptionsService = {};

        var resource = getResource();

        function getResource() {
            return 'ps_typeDescriptions';

        }

        TypeDescriptionsService.getAll = function (groupID, typeID, lang) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource + '?tid=' + typeID + '&lang=' + lang
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeDescriptionsService.create = function (data, showLang) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource + '?showLang=' + showLang,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeDescriptionsService.removeDescription = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeDescriptionsService.editDescription = function (data) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        TypeDescriptionsService.getDescription = function (data) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        TypeDescriptionsService.sort = function (data) {

            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        TypeDescriptionsService.getUploadUrl = function () {
            return $config.API_URL + [resource, 'files'].join('/');
        };

        TypeDescriptionsService.getFiles = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'files'].join('/')

            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise
        };

        TypeDescriptionsService.setDescriptionFile = function (file) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'files'].join('/'),
                data: file
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise
        };

        TypeDescriptionsService.getDescriptionFile = function (descID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'descFiles', descID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise
        };

        TypeDescriptionsService.removeDescriptionFile = function (fileID) {
            var def = $q.defer();
            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, 'files', fileID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise
        };

        return TypeDescriptionsService;
    });
