javascript
'use strict';

angular.module('digitalprint.services')
    .service('PsGroupDescriptionService', function ($q, $http, $config, Restangular, $cacheFactory) {
        
        var PsGroupDescriptionService = {};

        PsGroupDescriptionService.getAll = function (groupUrl) {
            // [BACKEND_ADVICE] This API call is heavy on logic and should be optimized
            return $http({
                method: 'GET',
                url: $config.API_URL + 'ps_groupDescriptions/groupDescriptionsPublic?groupUrl=' + groupUrl,
                cache: $cacheFactory.get('groupDescriptionCache')
            }).then(function (response) {
                return response.data;
            }, function (errorResponse) {
                return $q.reject(errorResponse);
            });
        };

        return PsGroupDescriptionService;

    });
