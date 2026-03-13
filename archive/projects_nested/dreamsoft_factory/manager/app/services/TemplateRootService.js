angular.module('digitalprint.services')
    .service('TemplateRootService', function ($rootScope, $q, $http, $config, Upload) {

        var TemplateRootService = {};

        var resource = 'templates';

        TemplateRootService.getAll = function () {

            var def = $q.defer();

            /**
             * @param {string} $config.API_URL
             */

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

        TemplateRootService.getAllVariables = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'variables'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        TemplateRootService.getTemplateVariables = function (templateID) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'templateVariables', templateID]
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
        };

        TemplateRootService.add = function (data) {

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

        TemplateRootService.addVariable = function (data) {

            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'variables'].join('/'),
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

        TemplateRootService.edit = function (data) {

            var def = $q.defer();

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
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TemplateRootService.editVariable = function (data) {

            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, 'variables'].join('/'),
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

        TemplateRootService.setTemplate = function (data) {
            console.log(data);
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'routeTemplates'].join('/'),
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

        TemplateRootService.getTemplates = function (routeID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'routeTemplates'].join('/') + '?routeID=' + routeID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TemplateRootService.removeTemplateFromRoute = function (templateID, routeID) {

            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, 'routeTemplates'].join('/') + '?routeID=' + routeID + '&templateID=' + templateID
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

        TemplateRootService.remove = function (templateID) {

            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, templateID].join('/')
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

        TemplateRootService.uploadFile = function (template) {
            return Upload.upload({
                url: $config.API_URL + [resource, 'upload', template.ID].join('/'),
                fileFormDataName: 'templateFile',
                file: template.file
            });
        };

        TemplateRootService.getFile = function (templateID) {
            return $config.API_URL + [resource, 'getFile', templateID].join('/');
        };

        TemplateRootService.getTemplateFile = function (templateID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getFile', templateID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TemplateRootService.setSource = function (data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'setSource'].join('/'),
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

        TemplateRootService.removeFile = function (template) {

            console.log( template );

            var root = 0;
            if( template.own === false ) {
                root = 1;
            }
            var data = {templateID: template.ID, root: root};

            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'removeFile'].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return TemplateRootService;

    });