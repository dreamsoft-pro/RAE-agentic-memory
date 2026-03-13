'use strict';

angular.module('digitalprint.services')
    .factory('GroupDescriptionsService', function ($q, $http, $config, Restangular, FileUploader) {

        var GroupDescriptionsService = {};

        var resource = getResource();

        function getResource() {
            return 'ps_groupDescriptions';

        }

        GroupDescriptionsService.getAll = function (groupID, lang) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '?gid=' + groupID + '&lang=' + lang
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupDescriptionsService.create = function (data, showLang) {
            var def = $q.defer();
            console.log('data');
            console.log(data);
            console.log(showLang);
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

        GroupDescriptionsService.removeDescription = function (id) {
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


        GroupDescriptionsService.editDescription = function (data) {
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

        GroupDescriptionsService.getDescription = function (data) {
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

        GroupDescriptionsService.sort = function (data) {

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

        GroupDescriptionsService.getUploadUrl = function () {
            return $config.API_URL + [resource, 'files'].join('/');
        };

        GroupDescriptionsService.getFiles = function () {
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

        GroupDescriptionsService.setDescriptionFile = function (file) {
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

        GroupDescriptionsService.getDescriptionFile = function (descID) {
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

        return GroupDescriptionsService;
    });
