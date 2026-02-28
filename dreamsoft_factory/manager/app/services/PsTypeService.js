'use strict';

angular.module('digitalprint.services')
    .service('PsTypeService', function ($q, $http, $config, Restangular, $cacheFactory) {

        var cache = $cacheFactory('ps_types');

        var TypeService = {};

        TypeService.getUploadUrl = function () {
            var resource = ['ps_types'];
            resource.push('uploadIcon');
            return $config.API_URL + resource.join('/');
        };

        TypeService.getAll = function (groupID, force) {
            var def = $q.defer();

            if (cache.get('collection' + groupID) && !force) {
                def.resolve(cache.get('collection' + groupID));
            } else {
                Restangular.all('ps_groups/' + groupID + '/ps_types').getList().then(function (data) {
                    cache.put('collection' + groupID, data.plain());
                    def.resolve(data.plain());
                }, function (data) {
                    def.reject(data);
                });
            }

            return def.promise;
        };

        TypeService.get = function (groupID, id) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + 'ps_groups/' + groupID + '/ps_types/' + id
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.getExclusions = function (groupID, typeID) {
            var def = $q.defer();
            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_product_exclusions';
            Restangular.all(resource).get('').then(function (data) {
                def.resolve(angular.copy(data));
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.add = function (groupID, item) {
            var def = $q.defer();

            Restangular.all('ps_groups/' + groupID + '/ps_types').doPOST(item).then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.edit = function (groupID, item) {
            var def = $q.defer();

            Restangular.all('ps_groups/' + groupID + '/ps_types').customPUT(item).then(function (data) {
                if (data.response) {
                    cache.remove('collection' + groupID);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        TypeService.editCardGuide = function (groupID, item) {

            var def = $q.defer();
            Restangular.all('ps_groups/' + groupID + '/ps_types').customPUT(item).then(function () {
                if (data.response) {
                    cache.remove('collection' + groupID);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.editDescription = function (groupID, item) {

            var def = $q.defer();
            Restangular.all('ps_groups/' + groupID + '/ps_types').customPut(item).then(function () {

                if (data.response) {
                    cache.remove('collection' + groupID);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        TypeService.remove = function (groupID, item) {
            var def = $q.defer();
            var data;

            Restangular.all('ps_groups/' + groupID + '/ps_types').one(item.ID + '').remove().then(function (data) {
                if (data.response) {
                    cache.remove('collection' + groupID); //usuwamy cache za każdym add, remove
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;

        };

        TypeService.sort = function (groupID, sort) {
            var def = $q.defer();

            Restangular.all('ps_groups/' + groupID + '/ps_types').one('sort').patch(sort).then(function (data) {
                if (data.response) {
                    cache.remove('collection' + groupID); //usuwamy cache za każdym add, remove
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.getRealizationTimes = function (groupID, typeID, force) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_rt_details';

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

        TypeService.setRealizationTime = function (groupID, typeID, item) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_rt_details';

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

        TypeService.removeRealizationTime = function (groupID, typeID, item) {
            var def = $q.defer();

            if (!item.details) {
                def.reject();
            }

            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_rt_details';

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

        TypeService.cacheRemove = function (groupID) {
            cache.remove('collection' + groupID); //usuwamy cache za każdym add, remove
        };

        TypeService.deleteIcon = function (typeID) {
            var def = $q.defer();

            var resource = ['ps_types'];
            resource.push('uploadIcon');

            Restangular.all(resource.join('/')).one(typeID + '').remove().then(function (data) {
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

        TypeService.getActiveTypes = function (groupID, force) {
            var def = $q.defer();

            Restangular.all('ps_groups/' + groupID + '/ps_types/getActiveTypes').getList().then(function (data) {
                def.resolve(data);
            }, function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.copy = function (ID) {
            var def = $q.defer();
            $http({
                method: 'GET',
                url: $config.API_URL + 'ps_types/copy/' + ID
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        TypeService.setQuestionOnly = function (groupID, typeID, isQuestionOnly) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_question';

            Restangular.all(resource).patch({isQuestionOnly:isQuestionOnly}).then(function (data) {
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

        TypeService.setUseAternatives = function (groupID, typeID, useAlternatives) {
            var def = $q.defer();

            var resource = 'ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_use_alternatives';

            Restangular.all(resource).patch({useAlternatives:useAlternatives}).then(function (data) {
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

        return TypeService;
    });
