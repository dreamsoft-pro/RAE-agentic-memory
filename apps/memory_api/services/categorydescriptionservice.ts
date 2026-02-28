javascript
'use strict';

angular.module('digitalprint.services')
    .service('CategoryDescriptionService', function ($q, $http, $config, Restangular, $cacheFactory) {
        
        var CategoryDescriptionService = {};

        CategoryDescriptionService.getAll = function (list) {
            // [BACKEND_ADVICE] Heavy logic should be handled in backend services
            return $q.resolve($http.get($config.API_URL + 'categoriesDescriptions/categoriesDescriptionsPublic?list=' + list, { cache: $cacheFactory.get('categoryCache') }))
                .then(function(response) {
                    return response.data;
                }, function(error) {
                    return $q.reject(error);
                });
        };

        return CategoryDescriptionService;

    });
