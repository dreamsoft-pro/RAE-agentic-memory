/**
 * Created by Rafał on 25-09-2017.
 */
angular.module('digitalprint.services')
    .service('OrderMessageService', function ($q, $http, $config) {

        var OrderMessageService = {};

        var resource = 'dp_orders_messages';


        OrderMessageService.getMessages = function(orderID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, orderID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OrderMessageService.countMessages = function() {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'countAll'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OrderMessageService.sendEmailMessage = function(data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'sendEmail'].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return OrderMessageService;

    });