'use strict';

angular.module('digitalprint.services')
    .service('PsConfigOptionService', ['Restangular', '$cacheFactory', '$q', '$config', '$http', 'PsPricelistService', 'PsPrintTypeService', 'PsWorkspaceService', function (Restangular, $cacheFactory, $q, $config, $http, PsPricelistService, PsPrintTypeService, PsWorkspaceService) {

        var cache = $cacheFactory('ps_options');

        var PsConfigOption = function (attrID) {
            this.attrID = attrID;
        };

        PsConfigOption.prototype.getResource = function () {
            return 'ps_attributes/' + this.attrID + '/ps_options';
        };

        PsConfigOption.prototype.getUploadUrl = function() {
            var resource = this.getResource() + '/uploadIcon';
            return $config.API_URL + resource;
        };

        PsConfigOption.prototype.getAll = function (force) {
            var def = $q.defer();

            var resource = this.getResource();

            if (cache.get(resource) && !force) {
                def.resolve(cache.get(resource));
            } else {
                Restangular.all(resource).getList().then(function (data) {
                    var plain = data.plain();
                    cache.put(resource, plain);
                    def.resolve(plain);
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        PsConfigOption.prototype.copy = function (optID) {
            var def = $q.defer();
            var resource = this.getResource();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'copy', optID].join('/')
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            });

            return def.promise;
        };

        PsConfigOption.prototype.getOne = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID;

            Restangular.one(resource).get().then(function (data) {
                if (data.ID) {
                    def.resolve(data.plain());
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.add = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).doPOST(item).then(function (data) {
                if (data.ID) {
                    cache.remove(resource);
                    def.resolve(data);
                }
                def.reject(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsConfigOption.prototype.edit = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).customPUT(item).then(function (data) {
                if (data.response) {
                    cache.remove(resource);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.remove = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    cache.remove(resource);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsConfigOption.prototype.sort = function (sortList) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).one('sortOptions').patch(sortList).then(function (data) {
                if (data.response === true) {
                    def.resolve(data);
                }
                def.reject(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getRealizationTimes = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionRealizationTimes';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.addRealizationTime = function (optID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionRealizationTimes';

            Restangular.all(resource).doPOST(item).then(function (data) {
                if (data.ID) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeRealizationTime = function (optID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionRealizationTimes';

            Restangular.all(resource).one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getOptionDescriptions = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionDescriptions' ;

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveOptionDescriptions = function (optID, items) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionDescriptions';
            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: items
            }).success(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getOperations = function (optID, controllerID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionOperations/'+controllerID;

            $http({
                method: 'GET',
                url: $config.API_URL + resource
            }).success(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        PsConfigOption.prototype.saveOperations = function (optID, controllerID, operations) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/optionOperations/'+controllerID;

            $http({
                method: 'PATCH',
                url: $config.API_URL + resource,
                data: {operations:operations}
            }).success(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getExclusions = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/exclusions';

            Restangular.all(resource).get('').then(function (data) {
                def.resolve(angular.copy(data));
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveExclusions = function (optID, exclusions) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/exclusions';

            Restangular.all(resource).patch(exclusions).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getIncreases = function (optID, controllerID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerID + '/ps_config_increases';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getRelatedIncreaseCount = function (optID, controllerID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerID + '/ps_config_related_increases_count';

            Restangular.all(resource).get('').then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };


        PsConfigOption.prototype.getAttributesForIncreases = function () {
            var def = $q.defer();
            var resource = this.getResource() + '//increaseControllers//ps_config_related_increases';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };
        PsConfigOption.prototype.getRelatedIncreases = function (optID, controllerId) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerId + '/ps_config_related_increases_list';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getPaperIncreases = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/0/ps_config_increases';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveRelatedIncreases = function (optID, controllerId, increases) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerId + '/ps_config_related_increases_list';

            Restangular.all(resource).patch(increases).then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveIncreases = function (optID, controllerID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerID + '/ps_config_increases';

            Restangular.all(resource).patch(item).then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeIncrease = function (optID, controllerID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/increaseControllers/' + controllerID + '/ps_config_increases';

            Restangular.all(resource).patch({remove: item.ID}).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.countIncreases = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/ps_countIncreases';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.countPrices = function (optID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/ps_countPrices';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getPrices = function (optID, controllerID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_prices';

            Restangular.all(resource).getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getDiscountPrices = function (optID, controllerID, discountGroupID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_prices/discountPrices/'+discountGroupID;

            Restangular.all(resource).getList().then(function (data) {
                cache.remove(resource);
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.savePrices = function (optID, controllerID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_prices';

            Restangular.all(resource).patch(item).then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removePrice = function (optID, controllerID, item) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_prices';

            Restangular.all(resource).patch({remove: item.ID}).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeDiscountPrice = function (optID, controllerID, item, discountGroupID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_prices';

            Restangular.all(resource).patch({remove: item.ID, discountGroupID: discountGroupID}).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.getDetailPrices = function (optID, controllerID) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_detailPrices';

            Restangular.all(resource).get('').then(function (data) {
                var result = {};
                if (data.ID !== undefined) {
                    result = Restangular.stripRestangular(data);
                }
                def.resolve(result);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.setDetailPrices = function (optID, controllerID, prices) {
            var def = $q.defer();
            var resource = this.getResource() + '/' + optID + '/priceControllers/' + controllerID + '/ps_detailPrices';

            Restangular.all(resource).patch(prices).then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeAllPrice = function (optID, priceControllerID, priceType) {
            var def = $q.defer();

            var removeResource = [
                this.getResource(),
                optID,
                'priceControllers',
                priceControllerID,
                'ps_prices',
                'removeAll',
                priceType
            ];

            var resource = removeResource.join('/');

            Restangular.one(resource).doDELETE().then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeAllDiscountPrice = function (optID, priceControllerID, priceType, discountGroupID) {
            var def = $q.defer();

            var removeResource = [
                this.getResource(),
                optID,
                'priceControllers',
                priceControllerID,
                'ps_prices',
                priceType,
                'ps_prices_remove',
                discountGroupID
            ];

            var resource = removeResource.join('/');

            Restangular.one(resource).doDELETE().then(function (data) {
                if (data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.removeIcon = function(optionID) {

            var def = $q.defer();

            var resource = this.getResource() + '/uploadIcon';

            Restangular.all(resource).one(optionID+'').remove().then(function(data) {
                if(data.response) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function(data) {
                def.reject(data);
            });

            return def.promise;

        };

        PsConfigOption.prototype.getEfficiency= function (optID, controllerID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID] .join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveEfficiency = function (optID, controllerID, data) {
            var def = $q.defer();
            $http({
                method: 'PUT',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID].join("/"),
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

        PsConfigOption.prototype.getEfficiencySpeeds = function (optID, controllerID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID , 'speeds'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.addEfficiencySpeed = function (optID, controllerID, speedData) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID ,'speeds'].join("/"),
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

        PsConfigOption.prototype.deleteEfficiencySpeed = function (optID, controllerID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID ,'speeds',id].join('/')
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

        PsConfigOption.prototype.getEfficiencySpeedChanges = function (optID, controllerID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID , 'speedChanges'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.addEfficiencySpeedChange = function (optID, controllerID, data) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID ,'speedChanges'].join("/"),
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

        PsConfigOption.prototype.deleteEfficiencySpeedChange = function (optID, controllerID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID ,'speedChanges',id].join('/')
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

        PsConfigOption.prototype.getEfficiencySideRelations = function (optID, controllerID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID , 'sideRelations'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.addEfficiencySideRelation = function (optID, controllerID, data) {
            var def = $q.defer();
            $http({
                method: 'POST',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID , 'sideRelations'].join("/"),
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

        PsConfigOption.prototype.deleteEfficiencySideRelation = function (optID, controllerID, id) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [this.getResource() , optID ,'efficiency' , controllerID , 'sideRelations',id].join('/')
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

        PsConfigOption.getControllerService = function (type) {
            if (type === 1) {
                return PsPricelistService;
            } else if (type === 2) {
                return PsPrintTypeService;
            } else if (type === 3) {
                return PsWorkspaceService;
            }
        };

        PsConfigOption.prototype.getRelativeOptionsFilter = function (optID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [this.getResource() , optID ,'relativeOptions' ].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.search = function (attrID, filter) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + ['attributeFilters', attrID].join('/'),
                data: filter
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PsConfigOption.prototype.saveRelativeOptionsFilter = function (optID, data) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [this.getResource() , optID ,'relativeOptions' ].join('/'),
                data:data
            }).success(function (data) {
                if(data.response){
                    def.resolve(data);
                }else{
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return PsConfigOption;

    }]);
