javascript
'use strict';

angular.module('digitalprint.services')
    .factory('ModelIconsService', function ($q, $http, $config, Restangular) {
        var ModelIconsService = {};

        // [BACKEND_ADVICE] getResource should be backend-agnostic and lean.
        function getResource() {
            return 'dp_ModelIconsExtensions';
        }

        const resource = getResource();

        ModelIconsService.getAll = function () {
            // [BACKEND_ADVICE] Simplify promise handling using then().
            return $http.get($config.API_URL + resource).then(
                function (response) { 
                    return response.data; 
                }, 
                function (errorResponse) { 
                    throw errorResponse; 
                }
            );
        };

        return ModelIconsService;
    });
