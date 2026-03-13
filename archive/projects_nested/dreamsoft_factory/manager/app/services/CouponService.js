/**
 * Created by Rafał on 20-06-2017.
 */
angular.module('digitalprint.services')
    .service('CouponService', function($rootScope, $q, $http, $config){

        var CouponService = {};

        function getResource() {
            return ['dp_coupons'];
        }

        CouponService.add = function(data){
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + getResource().join('/'),
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        CouponService.addProduct = function(data){
            var def = $q.defer();

            var resource = getResource();
            resource.push('products');

            $http({
                method: 'POST',
                url: $config.API_URL + resource.join('/'),
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        CouponService.deleteProduct = function(ID){
            var def = $q.defer();

            var resource = getResource();
            resource.push('products');
            resource.push(ID);

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource.join('/')
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        CouponService.delete = function(ID){
            var def = $q.defer();

            var resource = getResource();
            resource.push(ID);

            $http({
                method: 'DELETE',
                url: $config.API_URL + resource.join('/')
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        return CouponService;

    });