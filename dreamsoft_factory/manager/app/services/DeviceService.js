angular.module('digitalprint.services')
    .factory('DeviceService', function ($rootScope, $q, $http, $config, $cacheFactory) {

        var DeviceService = {};

        var resource = 'devices';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        DeviceService.getAll = function (force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                cache.put('collection', data);
                getAllDef.resolve(data);
            }).error(function (data) {
                getAllDef.reject(data);
            });

            return getAllDef.promise;
        };

        DeviceService.get = function (id) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '/' + id
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.create = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
            }).success(function (data) {
                if (data.ID) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.update = function (module) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: module
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.updateEfficiency = function (data) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource +'/deviceEfficiency',
                data: data
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.remove = function (id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, id].join("/")
            }).success(function (data) {
                if (data.response) {
                    cache.remove('collection');
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.ongoings = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceOngoings'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.ongoingsSort = function (deviceID, sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, deviceID, 'deviceOngoings', 'sort'].join("/"),
                data: sort
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

        DeviceService.ongoingMove = function (deviceID, ongoingID, newDeviceID) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, deviceID, 'deviceOngoings', ongoingID, 'moveOngoings'].join("/"),
                data: {newDeviceID: newDeviceID}
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

        DeviceService.skills = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceSkills'].join("/")
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

        DeviceService.same = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'sameDevices', deviceID].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.setSame = function (deviceID, devices) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sameDevices', deviceID].join("/"),
                data: devices
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.countOngoings = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'countOngoings'].join("/") + '?date=' + (new Date().getTime())
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };
		
		DeviceService.countOngoingsPlanned = function() {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'countOngoingsPlanned'].join("/")
            }).success(function(data) {
                def.resolve(data);
            }).error(function(data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.countFilteredOngoings = function (deviceID, finished) {
            var def = $q.defer();

            var urlParam = '?deviceID='+deviceID+'&finished='+finished;

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'countFilteredOngoings'].join("/") + urlParam
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.sort = function (sort) {
            var def = $q.defer();

            $http({
                method: 'PATCH',
                url: $config.API_URL + [resource, 'sort'].join('/'),
                data: sort
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.getSpeeds = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceSpeeds'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.addSpeed = function (deviceID, speedData) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, deviceID, 'deviceSpeeds'].join("/"),
                data: speedData
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

        DeviceService.deleteSpeed = function (deviceID, speedID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource,deviceID,'deviceSpeeds',speedID].join('/')
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

        DeviceService.getSpeedChanges = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceSpeedChanges'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.saveSpeedChange= function (deviceID, data) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, deviceID, 'deviceSpeedChanges'].join("/"),
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

        DeviceService.deleteSpeedChange = function (deviceID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource,deviceID,'deviceSpeedChanges',id].join('/')
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

        DeviceService.getSideRelations = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceSideRelations'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.addSideRelation= function (deviceID, data) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, deviceID, 'deviceSideRelations'].join("/"),
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

        DeviceService.deleteSideRelation = function (deviceID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource,deviceID,'deviceSideRelations',id].join('/')
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

        DeviceService.getPrices = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'devicePrices'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.addPrice = function (deviceID, priceData) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, deviceID, 'devicePrices'].join("/"),
                data: priceData
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

        DeviceService.deletePrice = function (deviceID, priceID) {
            var def = $q.defer();


            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource,deviceID,'devicePrices',priceID].join('/')
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

        DeviceService.getSettings = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceSettings'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.saveSettings= function (deviceID, data) {
            var def = $q.defer();
            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, deviceID, 'deviceSettings'].join("/"),
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

        DeviceService.getServices = function (deviceID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, deviceID, 'deviceServices'].join("/")
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        DeviceService.addService= function (deviceID, data) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [resource, deviceID, 'deviceServices'].join("/"),
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

        DeviceService.deleteService = function (deviceID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource,deviceID,'deviceServices',id].join('/')
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
        DeviceService.getWorkUnits = function () {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + resource + '/' + 'getWorkUnits'
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        var speedUnits = {sheet: 'ark', squareMeter: 'm2', perimeter: 'mb', set: 'szt',projectSheets:'ark',every_sheet_separate:'ark', collectingFolds:'falce', folds:'falce'};

        DeviceService.getSpeedUnit=function(unit){
            if(speedUnits[unit]) {
                return speedUnits[unit];
            }
            return 'unit'
        };
        return DeviceService;
    });
