/**
 * Created by Rafał on 13-09-2017.
 */
angular.module('digitalprint.services')
    .factory('DpAddressService', function ($rootScope, $q, $config, $http) {

        var AddressService = {};

        AddressService.getDefaultAddress = function (userID, type) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url:  $config.API_URL + 'dp_addresses' + '/' + userID + '?type=' + type
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return AddressService;

    });