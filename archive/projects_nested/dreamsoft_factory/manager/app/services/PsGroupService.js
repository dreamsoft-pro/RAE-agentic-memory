'use strict';

angular.module('digitalprint.services')
    .service('PsGroupService', function ($q, $http, $config, Restangular, CacheService) {

        var GroupService = {};

        var cacheResolve = new CacheService('ps_groups');

        GroupService.getAll = function (params, options) {
            var def = $q.defer();
            options = options || {};

            var restangularPromise = Restangular.all('ps_groups', params);

            cacheResolve.getList(restangularPromise, options).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupService.getUploadUrl = function () {
            var resource = ['ps_groups'];
            resource.push('uploadIcon');
            return $config.API_URL + resource.join('/');
        };

        GroupService.get = function (id) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + 'ps_groups/' + id
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupService.add = function (item) {
            var def = $q.defer();

            Restangular.all('ps_groups').doPOST(item).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupService.edit = function (item) {
            var def = $q.defer();
            Restangular.all('ps_groups').customPUT(item).then(function (data) {
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

        GroupService.editCardGuide = function (item) {

            var def = $q.defer();
            Restangular.all('ps_groups').customPUT(item).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupService.remove = function (item) {
            var def = $q.defer();

            Restangular.all('ps_groups').one(item.ID + '').remove().then(function (data) {
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

        GroupService.getRealizationTimes = function (groupID, force) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_rt_details';

            Restangular.all(resource).getList().then(function (data) {
                if (data) {
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        GroupService.setRealizationTime = function (groupID, item) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_rt_details';

            Restangular.all(resource).patch(item).then(function (data) {
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

        GroupService.removeRealizationTime = function (groupID, item) {
            var def = $q.defer();

            if (!item.details) {
                def.reject();
            }

            var resource = 'ps_groups/' + groupID + '/ps_rt_details';

            Restangular.all(resource).one(item.details.ID + '').remove().then(function (data) {
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

        GroupService.deleteIcon = function (groupID) {
            var def = $q.defer();

            var resource = ['ps_groups'];
            resource.push('uploadIcon');

            Restangular.all(resource.join('/')).one(groupID + '').remove().then(function (data) {
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

        GroupService.getForSelect = function (groupID) {
            var def = $q.defer();

            var resource = ['ps_groups'];
            resource.push('groupsForSelect');

            Restangular.all(resource.join('/')).one(groupID + '').remove().then(function (data) {
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

        GroupService.getActiveGroups = function (params, options) {
            var def = $q.defer();
            options = options || {};

            var restangularPromise = Restangular.all('ps_groups/getActiveGroups', params);

            cacheResolve.getList(restangularPromise, options).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return GroupService;
    });