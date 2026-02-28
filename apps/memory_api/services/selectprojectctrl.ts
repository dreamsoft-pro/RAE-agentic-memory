javascript
'use strict';

import { getOneForView as psTypeGetOneForView } from '@/lib/api/ps-type-service';
import { getProjectsForTypes as photoFolderGetProjectsForTypes } from '@/lib/api/photo-folder-service';
import { Notification } from '@lib/notification';

angular.module('dpClient.app')
    .controller('category.SelectProjectCtrl', function ($scope, $rootScope, $filter, $stateParams) {
        const typeUrl = $stateParams.typeurl;
        const groupUrl = $stateParams.groupurl;

        $scope.type = {};
        $scope.mainThemes = [];

        function init() {
            psTypeGetOneForView(groupUrl, typeUrl).then(dataType => {
                $scope.type = dataType;
            });

            photoFolderGetProjectsForTypes([]).then(mainThemesData => {
                $scope.mainThemes = mainThemesData;
            });
        }

        init();
    });
