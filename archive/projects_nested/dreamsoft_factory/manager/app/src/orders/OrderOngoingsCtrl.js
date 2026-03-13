angular.module('digitalprint.app')
    .controller('orders.OrderOngoingsCtrl', function ($state, $rootScope, $filter, $scope, Notification, $modal, OrderService, OperationService, DeviceService, focus) {


        $scope.form = {};
        $scope.sortChange = false;
        $scope.currentOrderID;

        function init() {

            $scope.sortableOptions = {
                stop: function (e, ui) {
                    $scope.sortChange = true;
                },
                axis: 'y',
                placeholder: 'success',
                handle: 'button.button-sort',
                cancel: ''
            };


            OperationService.getAll().then(function (data) {
                $scope.operations = data;
            });
            DeviceService.getAll().then(function (data) {
                $scope.devices = data;
            });

            if ($state.params.orderID) {
                $scope.form.orderID = $state.params.orderID;
                $scope.getOngoings();
            }

            focus('productionPanelInput');

        }

        $scope.go = function () {
            if ($state.params.orderID == $scope.form.orderID) {
                $scope.getOngoings();
                focus('productionPanelInput');
            } else {
                $state.go($state.current.name, {orderID: $scope.form.orderID});
            }
        };

        $scope.getOngoings = function () {

            OrderService.ongoings($scope.form.orderID).then(function (data) {
                $scope.currentOrderID = _.clone($scope.form.orderID);
                $scope.tasks = data;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.changeOngoing = function (task, state) {
            var ongoing = {};
            ongoing.state = state;
            if (state === 3) {
                ongoing.finished = 1;
            }

            OrderService.patchOngoings($scope.form.orderID, task.ID, ongoing).then(function (data) {
                task = _.extend(task, ongoing);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + data.info);
            });
        };

        $scope.refresh = $scope.getOngoings;

        $scope.sortCancel = function () {
            $scope.refreshTypes();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.types, function (item) {
                result.push(item.ID);
            });

            OrderService.sort(currentGroupID, result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };

        init();

    });