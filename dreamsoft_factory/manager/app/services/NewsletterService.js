angular.module('digitalprint.services')
    .service('NewsletterService', function($rootScope, $q, $http, $config){

        var NewsletterService = {};

        var resource = 'dp_newsletter';

        NewsletterService.getAll = function(){
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        NewsletterService.export = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource +'/export'
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

        return NewsletterService;

    });