javascript
'use strict';

const { getPhotos, updateFolder } = require('@/lib/api');
const BACKEND_ADVICE = '// [BACKEND_ADVICE]';

angular.module('dpClient.app')
    .controller('client-zone.MyPhotosCtrl', function ($scope, $state, $filter, Notification, $rootScope, ClientZoneWidgetService,
                                                      TemplateRootService, $modal, PhotoFolderService, $stateParams,
                                                      AuthService, $window, $q, CanvasService, $config) {

        $scope.photos = [];
        $scope.folder = {};
        $scope.actualPhoto = {};
        $scope.sliderOn = false;
        $scope.slider = {
            value: 0,
            options: {
                floor: -100,
                ceil: 100
            }
        };
        $scope.slider.type = null;
        $scope.textOn = false;

        $scope.folderId = $stateParams.folderid;

        $scope.sort = {'name': 1};

        BACKEND_ADVICE // Fetch photos logic should be moved to backend service
        $scope.getPhotos = async () => {
            try {
                const response = await getPhotos($scope.folderId);
                $scope.photos = response.data;
            } catch (error) {
                Notification.error(error.message);
            }
        };

        $scope.updateFolder = async () => {
            try {
                await updateFolder($scope.folder);
                Notification.success('Folder updated successfully');
            } catch (error) {
                Notification.error(error.message);
            }
        };

        $scope.pageSizeSelect = ClientZoneWidgetService.getPageSizeSelect();

});
