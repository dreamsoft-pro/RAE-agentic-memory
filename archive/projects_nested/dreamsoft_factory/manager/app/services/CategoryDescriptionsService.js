'use strict';

angular.module('digitalprint.services')
    .factory('CategoryDescriptionsService', function ($q, $http, $config, Restangular, FileUploader) {

        var CategoryDescriptionsService = {};

        var resource = getResource();

        function getResource() {
            return 'categoriesDescriptions';

        }

        CategoryDescriptionsService.getAll = function (catID, lang) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '?category_id=' + catID + '&lang=' + lang
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        CategoryDescriptionsService.create = function (data, showLang) {
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

        CategoryDescriptionsService.removeDescription = function (id) {
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

        CategoryDescriptionsService.editDescription = function (data) {
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

        CategoryDescriptionsService.getDescription = function (data) {
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

        CategoryDescriptionsService.sort = function (data) {

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

        CategoryDescriptionsService.getUploadUrl = function () {
            return $config.API_URL + [resource, 'files'].join('/');
        };

        CategoryDescriptionsService.getFiles = function () {
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

        CategoryDescriptionsService.setDescriptionFile = function (file) {
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

        CategoryDescriptionsService.getDescriptionFile = function (descID) {
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

        CategoryDescriptionsService.removeDescriptionFile = function (fileID) {
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

        return CategoryDescriptionsService;
    });
