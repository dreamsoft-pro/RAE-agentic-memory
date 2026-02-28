'use strict';

angular.module('digitalprint.services')
    .factory('PsPageService', function ($q, Restangular, $cacheFactory, $http, $config) {

        var cache = $cacheFactory('ps_pages');

        var PageService = function (groupID, typeID) {
            this.groupID = groupID;
            this.typeID = typeID;
            this.resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_pages';
        };


        PageService.prototype.getAll = function (force) {
            var def = $q.defer();
            var _this = this;

            if (cache.get(this.resource) && !force) {
                def.resolve(cache.get(this.resource));
            } else {
                Restangular.all(_this.resource).getList().then(function (data) {
                    cache.put(_this.resource, data.plain());
                    def.resolve(data.plain());
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        PageService.prototype.addPage = function (item) {
            var def = $q.defer();
            var _this = this;

            Restangular.all(_this.resource).patch(item).then(function (data) {
                if (data.item) {
                    cache.remove(_this.resource); //usuwamy cache za każdym add, remove
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PageService.prototype.setSimilarPage = function (similarPage) {
            var def = $q.defer();
            var _this = this;

            $http({
                method: 'PATCH',
                url: $config.API_URL + _this.resource,
                data: {action: 'similarPage', similarPage: similarPage}
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

        PageService.prototype.remove = function (item) {
            var def = $q.defer();
            var _this = this;

            Restangular.all(_this.resource).one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    cache.remove(_this.resource); //usuwamy cache za każdym add, remove
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        PageService.prototype.getCustomNames = function () {
            var def = $q.defer();

            var resource = 'ps_pages';

            Restangular.all(resource).one('customName', this.typeID).get().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        PageService.prototype.setCustomNames = function (names) {
            var def = $q.defer();

            var resource = 'ps_pages/customName/' + this.typeID;

            Restangular.all(resource).patch({'names': names}).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return PageService;

    });