'use strict';

angular.module('digitalprint.app')
    .controller('contents.CategoriesSortCtrl', function ($scope, $rootScope, $filter, $modal, DpCategoryService,
                                                         Notification, $stateParams) {


        var categoryID = $scope.categoryID = parseInt($stateParams.categoryid);

        function init() {

            $scope.sortChange = false;
            $scope.items = [];

            $scope.sortableOptions = {
                opacity: 0.7,
                axis: 'x,y',
                placeholder: {
                    element: function (currentItem) {
                        var style ='';
                        if (angular.isDefined(currentItem)) {
                            style = 'height: ' + currentItem.context.offsetHeight + 'px;'; // pobrana wysokość
                        } else {
                            style = 'height: 150px;';
                        }

                        return $('<div style="' + style + ';" class="col-xs-4 col-md-2 alert-info"></div>')[0];
                    },
                    update: function (container, p) {
                        return;
                    }
                },
                stop: function (e, ui) {
                    _.each($scope.items, function (item, index) {

                        item.sort = index;

                    });
                    // console.log($scope.items);
                    $scope.sortChange = true;
                },
                handle: 'button.button-sort',
                cancel: ''
            };

            getContains();

            getCategory();

        }

        init();

        function getContains() {
            DpCategoryService.getContainsAdmin($scope.categoryID).then(function (data) {

                $scope.items = data;

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

        function getCategory() {
            DpCategoryService.getOne(categoryID).then(function(category) {

                $scope.category = category;

            });
        }

        $scope.sortSave = function () {
            var result = [];
            var items = _.sortBy($scope.items, function (p) {
                return p.sort;
            });
            // console.log(items);
            _.each(items, function (item, index) {
                result.push(item.ID);
            });

            // console.log(result);

            DpCategoryService.sortItems(result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        $scope.sortCancel = function () {
            $scope.sortChange = false;
        };

    });
