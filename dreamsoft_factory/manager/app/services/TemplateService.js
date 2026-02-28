/**
 * Created by Rafał on 25-04-2017.
 */
angular.module('digitalprint.services')
    .service('TemplateService', function ($rootScope, $q, $http, $config, Upload) {

        var TemplateService = {};

        var resource = 'local_templates';

        TemplateService.getAll = function () {

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

        TemplateService.add = function (data) {

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

       TemplateService.edit = function (data) {

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

        TemplateService.uploadFile = function (template) {
            return Upload.upload({
                url: $config.API_URL + [resource, 'upload', template.ID].join('/'),
                fileFormDataName: 'templateFile',
                file: template.file
            });
        };

        TemplateService.setSource = function (data) {
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

        TemplateService.getFile = function (templateID) {
            return $config.API_URL + [resource, 'getFile', templateID].join('/');
        };

        TemplateService.uploadFile = function (template) {
            return Upload.upload({
                url: $config.API_URL + [resource, 'upload', template.ID].join('/'),
                fileFormDataName: 'templateFile',
                file: template.file
            });
        };

        TemplateService.remove = function (templateID) {

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

        TemplateService.removeFile = function (template) {
            var root = 0;
            if (template.own === false) {
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

        return TemplateService;

    });
