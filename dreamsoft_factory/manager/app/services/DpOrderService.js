angular.module('digitalprint.services')
    .factory('DpOrderService', function ($q, $http, $config) {

        var DpOrderService = {};

        var resource = 'dp_orders';

        DpOrderService.getAll = function () {

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

        DpOrderService.get = function (id, ver) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + resource,
                params: {ID: id, ver: ver}
            }).success(function (data) {
                if (data.length === 1) {
                    def.resolve(data[0]);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.patch = function (id, data) {

            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, id].join('/'),
                data: data
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

        DpOrderService.togglePaid = function (id, data) {

            var def = $q.defer();

            if( data.paid !== undefined ) {
                data.paid = data.paid ? 1 : 0;
            }

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, id].join('/'),
                data: data
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

        DpOrderService.getOrder = function (id) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource + '?production=1&isOrder=1'].join('/'),
                params: {ID: id}
            }).success(function (data) {
                if (data.length === 1) {
                    def.resolve(data[0]);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.makeOrder = function (orderID, data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'order', orderID].join('/'),
                data: data
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

        DpOrderService.updateAddress = function (data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'updateAddress'].join('/'),
                data: data
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

        DpOrderService.updateVatAddress = function (data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'updateVatAddress'].join('/'),
                data: data
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

        DpOrderService.placeOrder = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'placeOrder'].join('/'),
                data: data
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

        DpOrderService.edit = function (id, data) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, id].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        DpOrderService.saveOffer = function (orderID, data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'saveOffer', orderID].join('/'),
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject()
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.sellerNotReady = function (type) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'sellerNotReady'].join('/') + '?type=' + type
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.addressAdd = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'saveOffer', orderID].join('/'),
                data: data
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject()
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.getAddresses = function (orderID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getAddresses', orderID].join('/')
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

        DpOrderService.paymentRemind = function(orderID) {
            var def = $q.defer();
              $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'paymentRemind', orderID].join("/")
              }).success(function(data) {
                def.resolve(data);
              }).error(function(data) {
                def.reject(data);
              });

            return def.promise;
        };

        DpOrderService.sendPaymentRemind = function (orderID, data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'paymentRemind', orderID].join("/"),
                data:data
              }).success(function(data) {
                def.resolve(data);
              }).error(function(data) {
                def.reject(data);
              });

            return def.promise;
        };

        DpOrderService.getOrderInvoiceAddress = function(orderID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'getOrderInvoiceAddress', orderID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.changeOrderPrice = function (orderID, data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'changeOrderPrice', orderID].join('/'),
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.restoreOrderPrice = function (orderID) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'restoreOrderPrice', orderID].join('/'),
                data: {}
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

        DpOrderService.fileReminder = function(orderID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'fileReminder', orderID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        DpOrderService.sendFileRemind = function (orderID, data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'fileReminder', orderID].join("/"),
                data:data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        return DpOrderService;

    });
