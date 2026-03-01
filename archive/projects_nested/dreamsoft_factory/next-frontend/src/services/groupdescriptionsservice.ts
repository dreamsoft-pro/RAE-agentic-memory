javascript
'use strict';

angular.module('digitalprint.services')
    .factory('GroupDescriptionsService', function ($q, $http, $config, Restangular, FileUploader) {

        var GroupDescriptionsService = {};

        // [BACKEND_ADVICE] Consider moving this to a backend service for better separation of concerns.
        var resource = getResource();

        function getResource() {
            return 'ps_groupDescriptions';
        }

        GroupDescriptionsService.getAll = function (groupID, lang) {
            const url = $config.API_URL + resource + '?gid=' + groupID + '&lang=' + lang;
            return $http({
                method: 'GET',
                url: url
            }).then(function (response) {
                return response.data;
            }, function (error) {
                throw error;
            });
        };

        return GroupDescriptionsService;

    });
