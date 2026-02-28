angular.module('digitalprint.services')
    .service('TemplateVariablesService', function ($q, $http, $config, Upload) {

        var TemplateVariablesService = {};

        var resource = 'templateVariables';

        TemplateVariablesService.getAll = function () {

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

        TemplateVariablesService.getTemplates = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getTemplates'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };
        TemplateVariablesService.getSelectors = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getSelectors'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };
        TemplateVariablesService.getGlobalVariables = function () {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getGlobal'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };
        TemplateVariablesService.getForRange = function (range, id) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getForRange'].join('/') + '?range=' + range + '&id=' + id
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };
        TemplateVariablesService.add = function (data) {

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

        TemplateVariablesService.edit = function (id, data) {

            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource+'/'+id,
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

        TemplateVariablesService.saveAssoc = function (data) {

            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource +'/assoc',
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

TemplateVariablesService.updateAssoc = function (id, data) {
            var update={};
            var def = $q.defer();
            $http({
                method: 'PUT',
                url: $config.API_URL + resource +'/assoc/'+id,
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


        TemplateVariablesService.remove = function (id) {

            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join('/')
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

        return TemplateVariablesService;

    });
