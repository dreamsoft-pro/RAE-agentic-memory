javascript
'use strict';

angular.module('digitalprint.services')
    .factory('HomepageBannerService', function ($q, $http, $config, Restangular) {
        var HomePageBannerService = {};

        // [BACKEND_ADVICE] Extract resource retrieval logic to a separate method for better maintainability and reusability.
        function getResource() {
            return 'homePageBanner';
        }

        // [BACKEND_ADvice] Use the extracted resource retrieval method here.
        const resource = getResource();

        HomePageBannerService.getAll = function () {
            const deferred = $q.defer();
            const apiUrl = $config.API_URL + resource + '/homePageBannerPublic';

            $http({
                method: 'GET',
                url: apiUrl
            }).then(
                (response) => { // Success callback
                    deferred.resolve(response.data);
                },
                (errorResponse) => { // Error callback
                    deferred.reject(errorResponse);
                }
            );

            return deferred.promise;
        };

        return HomePageBannerService;
    });
