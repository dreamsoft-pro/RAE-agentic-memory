angular.module('digitalprint.services')
    .factory('OngoingService', function($q, $http, $config){

        var OngoingService = {};

        var resource = 'ongoings';

        OngoingService.patchOngoings = function(ongoingID, data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, ongoingID].join("/"),
                data: data
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.ongoingsLogs = function(ongoingID, isAdditional) {
            var def = $q.defer();

            var path = 'logs';
            if(isAdditional){
                path = 'logsAdditional';
            }
            
            $http({
                method: 'GET',
                url: $config.API_URL + [resource, path, ongoingID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.patchWorkplace = function(workplace) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'taskWorkplaces'].join("/"),
                data: workplace
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getTaskWorkplaces = function (itemID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'taskWorkplaces', itemID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getOperatorsWithSkills = function (taskID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'operatorsWithSkills', taskID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getAllOperators = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'operators'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.patchOperator = function(operator) {
            var def = $q.defer();
            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'operator'].join("/"),
                data: operator
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.patchOperatorAdditional = function(operator) {
            var def = $q.defer();
            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'operatorAdditional'].join("/"),
                data: operator
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.showForItem = function(itemID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'showForItem', itemID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.saveProgress = function(data) {

            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'progress'].join("/"),
                data: data
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;

        };
		
		OngoingService.sort = function(sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sortProd'].join('/'),
                data: sort
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.addAdditionalOperation = function(operation) {
            var def = $q.defer();
        
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'additionalOperation'].join("/"),
                data: operation
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });
        
            return def.promise;
        };

        OngoingService.patchOngoingAdditional = function(data) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'additionalOperation', data.ID].join("/"),
                data: data
            }).success(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getAlreadyStartedTasks = function(ongoingID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'alreadyStartedTasks', ongoingID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getFinishedByOperator = function(operatorID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'finishedByOperator', operatorID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getOperatorLogs = function(operatorID, dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getOperatorLogs', operatorID].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getAllOperatorLogs = function(dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getAllOperatorLogs'].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getDeviceLogs = function(deviceID, dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getDeviceLogs', deviceID].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getAllDeviceLogs = function(dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getAllDeviceLogs'].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getOrderLogs = function(orderID, dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getOrderLogs', orderID].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getOperationsLogs = function(dates) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'getOperationsLogs'].join("/"),
                data: dates
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getOngoingsForCalcProduct = function(calcProductID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'ongoingsForCalcProduct', calcProductID].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.getSettings = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'productionSettings'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        OngoingService.saveSettings= function (data) {
            var def = $q.defer();
            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, 'productionSettings'].join("/"),
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

        OngoingService.sortOrderOnDevice = function(sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'ongoingsOrder'].join('/'),
                data: sort
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        return OngoingService;
    });