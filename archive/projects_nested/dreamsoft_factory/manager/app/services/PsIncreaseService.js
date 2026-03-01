'use strict';

angular.module('digitalprint.services')
    .factory('PsIncreaseService', function ($q, Restangular, $cacheFactory) {

        var cache = $cacheFactory('ps_increases');

        var IncreaseService = function (groupID, typeID) {
            this.groupID = groupID;
            this.typeID = typeID;
            this.resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_increases';
        };


        IncreaseService.prototype.getAll = function (typeID, force) {
            var def = $q.defer();
            var _this = this;

            var resource = [this.resource, typeID].join('/');

            if (cache.get(this.resource) && !force) {
                def.resolve(cache.get(resource));
            } else {
                Restangular.all(resource).getList().then(function (data) {
                    cache.put(resource, data.plain());
                    def.resolve(data.plain());
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };


        IncreaseService.prototype.save = function (item) {
            var def = $q.defer();
            var _this = this;

            Restangular.all(_this.resource).patch(item).then(function (data) {
                if (data.response) {
                    cache.remove(_this.resource);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        IncreaseService.prototype.remove = function (item) {
            var def = $q.defer();
            var _this = this;

            Restangular.all(_this.resource).patch({remove: item.ID}).then(function (data) {
                if (data.response) {
                    cache.remove(_this.resource);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };


        return IncreaseService;

    });