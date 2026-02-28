javascript
'use strict';

angular.module('digitalprint.services')
    .factory('TypePatternService', function ($q, $http, $config) {

        var TypePatternService = {};
        var resource = getResource();

        // [BACKEND_ADVICE] Consider moving the resource retrieval logic to a backend service if it becomes complex.
        
        function getResource() {
            return 'ps_patterns';
        }

        TypePatternService.getUploadUrl = function () {
            return $config.API_URL + [resource].join('/');
        };

        TypePatternService.getList = function (typeID, descID) {

            var params = {
                typeID: typeID,
                descID: descID
            };

            // [BACKEND_ADVICE] This API call should be verified against the backend capabilities.
            
            return $http({
                method: 'GET',
                url: $config.API_URL + [resource, 'patternsPublic'].join('/'),
                params: params
            }).then(function (response) {
                return response.data;
            }, function (errorResponse) {
                throw errorResponse;
            });
        };

        return TypePatternService;

    });
