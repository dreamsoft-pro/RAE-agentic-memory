'use strict';
angular.module('digitalprint.app')
    .controller('customerservice.NewsletterCtrl', function ($scope, $filter, Notification, $timeout, ApiCollection,
                                                         PsFormatService, PsTypeService, PsGroupService, NewsletterService,
                                                         CurrencyService, $modal) {

        $scope.newsletters = [];

        function init() {
            NewsletterService.getAll().then(function (data) {
                console.log(data);
                $scope.newsletters = data;
            });
        }

        init();

        $scope.search = function () {
            var newFilter = {};
            for(var filter in $scope.filterData){
                if($scope.filterData[filter] != ''){
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            $scope.filterData = newFilter;
        };

        $scope.exportNewsletter = function () {
            NewsletterService.export().then(function (data) {
                if (data.response) {
                    $modal.open({
                        templateUrl: 'shared/templates/modalboxes/files.html',
                        scope: $scope,
                        controller: function ($scope, $modalInstance) {
                            $scope.filesTitle = 'translation_export';
                            $scope.files = [data.url];
                            $scope.fileLabel = 'filesLabel';
                        }
                    });
                } else {
                    Notification.error(Notification.error($filter('translate')('error')));
                }
            });
        };

    });