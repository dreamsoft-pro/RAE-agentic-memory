angular.module('digitalprint.services')
    .service('PsPrintTypeWorkspaceService', function ($q, $rootScope, $http, $config) {

        var PsPrintTypeWorkspaceService = {};

        var resource = 'ps_printTypeWorkspaces';

        PsPrintTypeWorkspaceService.getAll = function (printTypeID, formatID) {

            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '/' + printTypeID + '?formatID=' + formatID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        return PsPrintTypeWorkspaceService;

    });

