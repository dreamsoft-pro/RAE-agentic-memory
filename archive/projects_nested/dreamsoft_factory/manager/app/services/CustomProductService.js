angular.module('digitalprint.services')
    .service('CustomProductService', function ($q, $http, $config) {

        var resource = 'dp_customProducts';

        var SubcategoryDescriptionsService = {};

        SubcategoryDescriptionsService.getOne = function (customProductID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getOne', customProductID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise
        };

        return SubcategoryDescriptionsService;

    });