'use strict';

angular.module('digitalprint.services')
    .factory('SubcategoryDescriptionsService', function ($q, $http, $config) {

        var SubcategoryDescriptionsService = {};

        var resource = getResource();

        function getResource() {
            return 'subcategoriesDescriptions';

        }

        SubcategoryDescriptionsService.getAll = function (catID, lang) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '?subcategory_id=' + catID + '&lang=' + lang
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        SubcategoryDescriptionsService.create = function (data, showLang) {
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

        SubcategoryDescriptionsService.removeDescription = function (id) {
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

        SubcategoryDescriptionsService.editDescription = function (data) {
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

        SubcategoryDescriptionsService.getDescription = function (data) {
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

        SubcategoryDescriptionsService.sort = function (data) {

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

        SubcategoryDescriptionsService.getUploadUrl = function () {
            return $config.API_URL + [resource, 'files'].join('/');
        };

        SubcategoryDescriptionsService.getFiles = function () {
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

        SubcategoryDescriptionsService.setDescriptionFile = function (file) {
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

        SubcategoryDescriptionsService.getDescriptionFile = function (descID) {
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

        SubcategoryDescriptionsService.removeDescriptionFile = function (fileID) {
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

        return SubcategoryDescriptionsService;
    });
