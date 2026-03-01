/**
 * Created by rafal on 10.02.17.
 */
'use strict';

angular.module('digitalprint.app')
    .controller('orders.StatusesCtrl', function ($scope, $timeout, $modal, $state, $filter, $config, Notification, DpStatusService) {

        $scope.statusForm = {};
        $scope.sortChange = false;
        $scope.statusTypes = [
            {ID: 0, name: 'default'},
            {ID: 1, name: 'start_status'},
            {ID: 2, name: 'end_status'},
            {ID: 3, name: 'rejected_status'}
        ];

        function init() {

            $scope.sortableOptions = {
                opacity: 0.7,
                axis: 'y',
                placeholder: 'success',
                stop: function (e, ui) {
                    _.each($scope.statuses, function (item, index) {
                        item.sort = index;
                    });
                    $scope.sortChange = true;
                },
                handle: 'button.button-sort',
                cancel: ''
            };

            DpStatusService.getAll().then(function (data) {
                $scope.statuses = data;
            });

        }

        $scope.refresh = function () {
            DpStatusService.getAll().then(function (data) {
                $scope.statuses = data;
            });
            $scope.sortChange = false;
        };

        $scope.save = function () {

            DpStatusService.add($scope.statusForm).then(function (data) {
                if (data.response === true) {

                    $scope.statuses.push(data.item);
                    $scope.statusForm = {};
                    Notification.success($filter('translate')('success'));

                } else {

                    Notification.error($filter('translate')('error'));

                }


            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.remove = function (status) {

            DpStatusService.remove(status.ID).then(function (data) {
                if (data.response) {
                    var idx = _.findIndex($scope.statuses, {ID: data.ID});
                    if (idx > -1) {
                        $scope.statuses.splice(idx, 1);
                        Notification.success($filter('translate')('success'));
                    }
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.edit = function (elem) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/edit-statuses.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.editForm = elem;

                    $scope.ok = function () {
                        DpStatusService.update($scope.editForm).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        });
                    }

                }

            });
        };

        $scope.sortCancel = function () {
            $scope.refresh();
        };

        $scope.sortSave = function () {

            var result = [];
            _.forEach($scope.statuses, function (elem) {
                result.push(elem.ID);
            });

            DpStatusService.sort(result).then(function (data) {
                $scope.sortChange = false;
            });
        };

        $scope.updateType = function (status) {
            var data = {ID: status.ID, type: status.type};
            DpStatusService.update(data).then(function (data) {
                Notification.success($filter('translate')('success'));
            });
        };

        init();

    });