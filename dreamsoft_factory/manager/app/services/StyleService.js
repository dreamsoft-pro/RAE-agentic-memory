angular.module('digitalprint.services')
    .factory('StyleService', function ($q, $http, $config) {

        var StyleService = {};

        StyleService.getMainFile = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + 'mainCssFile'
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        StyleService.saveMainFile = function (content) {
            var def = $q.defer();

            var data = {
                content: content
            };

            $http({
                method: 'POST',
                url: $config.API_URL + 'mainCssFile',
                data: data
            }).success(function (responseData) {
                def.resolve(responseData);
            }).error(function (responseData) {
                def.reject(responseData);
            });

            return def.promise;
        };

        return StyleService;

    });