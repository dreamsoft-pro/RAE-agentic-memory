'use strict';

angular.module('digitalprint.services')
    .factory('PsFormatService', function ($q, Restangular, $cacheFactory) {

        var cache = $cacheFactory('ps_formats');

        var FormatService = function (groupID, typeID) {
            this.groupID = groupID;
            this.typeID = typeID;
        };

        FormatService.prototype.getResource = function () {
            return 'ps_groups/' + this.groupID + '/ps_types/' + this.typeID + '/ps_formats';
        };

        FormatService.prototype.getAll = function (force) {
            var def = $q.defer();

            var resource = this.getResource();

            if (cache.get(resource) && !force) {
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

        FormatService.prototype.sort = function (sort) {
            var def = $q.defer();
            var resource = this.getResource();


            Restangular.all(resource).one('sortFormats').patch(sort).then(function (data) {
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

        FormatService.prototype.add = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).doPOST(item).then(function (data) {
                if (data.ID) {
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

        FormatService.prototype.edit = function (item) {
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

        FormatService.prototype.remove = function (item) {
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

        FormatService.prototype.setPrintTypes = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).one(item.ID + '').patch({
                action: 'setPrintTypes',
                printTypes: item.printTypes
            }).then(function (data) {
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

        FormatService.prototype.setPrintTypeWorkspaces = function (item) {
            var def = $q.defer();

            var resource = this.getResource();

            Restangular.all(resource).one(item.formatID + '').patch({
                action: 'setPrintTypeWorkspaces',
                workspaces: item.workspaces,
                printTypeID: item.printTypeID
            }).then(function (data) {
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

        FormatService.prototype.getPublic = function (complexID, force) {
            var def = $q.defer();

            var resource = this.getResource() + '/formatsPublic/' + complexID;

            if (cache.get(resource) && !force) {
                def.resolve(cache.get(resource));
            } else {
                Restangular.all(resource).getList().then(function (data) {
                    cache.put(resource, data.plain()); // nie zwracamy plain bo potrzebujemy obiekt do put
                    def.resolve(data.plain());
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        FormatService.prototype.getCustomNames = function () {
            var def = $q.defer();

            var resource = 'ps_formats';

            Restangular.all(resource).one('customName', this.typeID).get().then(function (data) {
                def.resolve(data.plain());
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        FormatService.prototype.setCustomNames = function (names) {
            var def = $q.defer();

            var resource = 'ps_formats/customName/' + this.typeID;

            Restangular.all(resource).patch({'names': names}).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return FormatService;
    });