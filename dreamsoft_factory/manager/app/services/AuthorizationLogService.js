angular.module('digitalprint.services')
    .factory('AuthorizationLogService', function($rootScope, $q, $http, $config, $cacheFactory) {

        var AuthorizationLogService = {};

        var resource = 'dp_authorizationLogs';

        AuthorizationLogService.deleteByUser = function (userID) {

            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, 'deleteByUser', userID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return AuthorizationLogService;
    });