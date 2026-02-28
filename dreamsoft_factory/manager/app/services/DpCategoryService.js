'use strict';

angular.module('digitalprint.services')
    .factory('DpCategoryService', function ($q, $http, $config, Restangular) {

        var DpCategoryService = {};
        var resource = getResource();

        function getResource() {
            return ['dp_categories'];
        }

        DpCategoryService.getUploadUrl = function () {
            var resource = getResource();
            resource.push('uploadIcon');
            return $config.API_URL + resource.join('/');
        };

        DpCategoryService.getAll = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.getOne = function (categoryID) {

            var def = $q.defer();

            var resource = getResource();
            resource.push(categoryID);

            $http({
                method: 'GET',
                url: $config.API_URL + resource.join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.getParents = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getParents'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.getSelectedToGroup = function (groupID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'selectedToGroup', groupID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.setSelectedToGroup = function (groupID, data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'setSelectedToGroup', groupID].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpCategoryService.getSelectedToType = function (typeID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'selectedToType', typeID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.setSelectedToType = function (typeID, data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'setSelectedToType', typeID].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.create = function (data) {

            var def = $q.defer();

            data.langs = _.extend({}, data.langs);

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpCategoryService.edit = function (data) {
            var def = $q.defer();

            data.onMainPage = data.onMainPage ? 1 : 0;

            data.langs = _.extend({}, data.langs);

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            });
            return def.promise;
        };

        DpCategoryService.delete = function (category) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource + '?ID=' + category.ID + '&parentID=' + category.parentID
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            });
            return def.promise;
        };

        DpCategoryService.forView = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'forView'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.sort = function (sort) {
            var def = $q.defer();

            Restangular.all(resource).one('sort').patch(sort).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpCategoryService.sortItems = function (sort) {
            var def = $q.defer();

            Restangular.all(resource).one('sortItems').patch(sort).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpCategoryService.getContains = function (categoryURL) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getContains', categoryURL].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.getContainsAdmin = function (categoryID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getContainsAdmin', categoryID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.categoryContains = function (relType) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'categoryContains', relType].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
                console.log(data);
            });

            return def.promise;
        };

        DpCategoryService.deleteIcon = function (categoryID) {
            var def = $q.defer();

            var resource = getResource();
            resource.push('uploadIcon');
            resource.push(categoryID);

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource.join('/')
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            });
            return def.promise;
        };

        return DpCategoryService;
    });