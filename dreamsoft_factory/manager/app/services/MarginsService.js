angular.module('digitalprint.services')
    .service('MarginsService', function ($rootScope, $q, $http, $config) {

        var MarginsService = {};

        var resource = 'margins';

        MarginsService.get = function (priceListID, natureID, groupID, typeID) {
            var def = $q.defer();
            var params = [resource, priceListID, natureID];
            if(groupID){
                params.push(groupID)
            }
            if(typeID){
                params.push('')
                params.push(typeID)
            }
            $http({
                method: 'GET',
                url: $config.API_URL + params.join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.add = function (margin) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource].join("/"),
                data: margin
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.edit = function (ID, margin) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, ID].join("/"),
                data: margin
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.removeMargin = function (ID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, ID].join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.getAllSuppliers = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + ['margins_supplier', 'getAllSuppliers'].join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.getSupplierMargins = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [ 'margins_supplier'].join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.addSupplierMargins = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + ['margins_supplier'].join("/"),
                data: data
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.editSupplierMargins = function (id, data) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + ['margins_supplier', id].join("/"),
                data: data
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };

        MarginsService.removeSupplierMargin = function (ID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + ['margins_supplier', ID].join("/")
            }).success(function (data) {
                def.resolve(data);
            });

            return def.promise;
        };
        return MarginsService;

    });
