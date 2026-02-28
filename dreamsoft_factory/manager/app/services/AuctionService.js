angular.module('digitalprint.services')
    .factory('AuctionService', function ($rootScope, Upload, $q, $http, $config, $cacheFactory) {

        var AuctionService = {};

        var resource = 'auctions';

        var cache = $cacheFactory(resource);

        var getAllDef = null;

        AuctionService.getAll = function (force) {
            if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
                getAllDef = $q.defer();
            } else {
                return getAllDef.promise;
            }

            if (cache.get('collection') && !force) {
                getAllDef.resolve(cache.get('collection'));
            } else {
                $http({
                    method: 'GET',
                    url: $config.API_URL + resource
                }).success(function (data) {
                    cache.put('collection', data);
                    getAllDef.resolve(data);
                }).error(function (data) {
                    getAllDef.reject(data);
                });
            }

            return getAllDef.promise;
        };

        AuctionService.getAuctions = function (filters) {
            var def = $q.defer();

            var url = [resource, 'getAuctions'].join('/');

            var qs = $.param(filters || {});
            if (qs) {
                url += '?' + qs;
            }

            $http({
                method: 'GET',
                url: $config.API_URL + url
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.uploadFile = function (auctionID, file) {

            return Upload.upload({
                url: $config.API_URL + [resource, auctionID, 'auctionFiles'].join('/'),
                fileFormDataName: 'auctionFile',
                file: file
            });
        };

        AuctionService.getAuctionFiles = function (auctionID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, auctionID, 'auctionFiles'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.getFile = function (auctionID, fileID) {
            return $config.API_URL + [resource, auctionID, 'auctionFiles', 'getFile', fileID].join('/');
        };

        AuctionService.removeFile = function (auctionID, fileID) {
            var def = $q.defer();

            $http({
                method: 'DELETE',
                url: $config.API_URL + [resource, auctionID, 'auctionFiles', fileID].join('/')
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

        AuctionService.forCompany = function (filters) {
            var def = $q.defer();

            var url = [resource, 'forCompany'].join('/');
            var qs = $.param(filters || {});
            if (qs) {
                url += '?' + qs;
            }

            $http({
                method: 'GET',
                url: $config.API_URL + url
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        /**
         *
         * @param {Integer} $auctionID GET
         * URL auctions/[auctionID]/auctionResponses
         */
        AuctionService.response = function (auctionID) {
            var def = $q.defer();

            var url = [resource, auctionID, 'auctionResponses'].join('/');

            $http({
                method: 'GET',
                url: $config.API_URL + url
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.allresponses = function (auctionID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, auctionID, 'auctionAllResponses'].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.selectWinner = function (auctionID, responseID) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, auctionID, 'auctionSelectWinner'].join('/'),
                data: {responseID: responseID}
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.responseWinner = function (auctionID) {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'responseWinner', auctionID].join('/')
            }).success(function (data) {
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuctionService.finishAuction = function (auctionID) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, 'finishAuction', auctionID].join('/'),
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

        AuctionService.order = function (auctionID, data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, 'order', auctionID].join('/'),
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


        /**
         *
         * @param {Integer} $auctionID GET
         * @param {String} $realizationDate POST
         * @param {String} $description POST
         * @param {Array} $items { itemID: {price: 123, finalPrice: 345} } POST
         * @param {Integer} $companyID POST/GLOBAL
         * @return {Array}
         * @example <br>
         * URL auctions/[auctionID]/auctionResponses
         */
        AuctionService.addResponse = function (auctionID, response) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + [resource, auctionID, 'auctionResponses'].join('/'),
                data: response
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

        /**
         *
         * @param {Integer} $auctionID GET
         * @param {String} $realizationDate POST
         * @param {String} $description POST
         * @param {Array} $items { itemID: {price: 123, finalPrice: 345} } POST
         * @param {Integer} $companyID POST/GLOBAL
         * @return {Array}
         * @example <br>
         * URL auctions/[auctionID]/auctionResponses
         */
        AuctionService.editResponse = function (auctionID, response) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + [resource, auctionID, 'auctionResponses'].join('/'),
                data: response
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

        AuctionService.create = function (data) {
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.API_URL + resource,
                data: data
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

        AuctionService.update = function (offer) {
            var def = $q.defer();

            $http({
                method: 'PUT',
                url: $config.API_URL + resource,
                data: offer
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

        // remove by ID
        AuctionService.remove = function (id) {
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

        AuctionService.isAuctionUser = function () {
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'isAuctionUser'].join("/")
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

        AuctionService.export = function (params) {
            var def = $q.defer();
            var _this = this;

            $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'export'].join("/"),
                params: params
            }).success(function (data) {
                if (data.response) {
                    data.apiUrl = $config.API_URL;
                    def.resolve(data);
                }
                def.reject(data);
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        return AuctionService;
    });
