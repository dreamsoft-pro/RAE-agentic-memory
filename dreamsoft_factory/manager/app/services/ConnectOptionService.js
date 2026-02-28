angular.module('digitalprint.services')
    .service('ConnectOptionService', function ($q, Restangular, $http, $config) {

        var ConnectOptionService = {};

        var resource = 'ps_connectOptions';

        ConnectOptionService.getAll = function () {
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

        ConnectOptionService.add = function (item) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: item
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

        ConnectOptionService.edit = function (item) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: item
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

        ConnectOptionService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
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

        ConnectOptionService.addToGroup = function (option) {
            var def = $q.defer();

            var params = {'connectID': option.connectID};

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'addToGroup', option.ID].join("/"),
                data: params
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

        ConnectOptionService.setPrice = function (connect, params) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'price', connect.ID].join("/"),
                data: params
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

        ConnectOptionService.getPrices = function (connect) {

            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'price', connect.ID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        ConnectOptionService.removePrice = function (price) {
            var def = $q.defer();

            console.log(price);

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, 'price', price.connectOptionID].join("/") + '?amount=' + price.amount
                //data: { 'amount': price.amount }
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

        return ConnectOptionService;
    });