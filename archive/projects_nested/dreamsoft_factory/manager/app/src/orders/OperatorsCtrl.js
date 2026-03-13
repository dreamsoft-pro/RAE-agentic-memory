angular.module('digitalprint.app')
    .controller('orders.OperatorsCtrl', function ($state, $rootScope, $filter, $scope, Notification, OperatorService,
                                                  OperationService, $modal, OrderService, DeviceService) {


        $scope.filterStates = ['planned', 'current', 'archived'];
        var stateMap = {planned: 1, current: 2, archived: 3};
        $scope.currentFilterState = $scope.filterStates[1];
        $scope.form = {};
        $scope.operators = [];
        $scope.currentOperatorID;

        $scope.showRows = 5000;
        $scope.logsConfig = {
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.logsCtrl.items = data;
            }
        };


        function init() {
            OperatorService.getAll().then(function (data) {
                $scope.operators = data;

                if ($state.params.operatorID) {
                    $scope.selectOperator();
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
            OperationService.getAll().then(function (data) {
                $scope.operations = data;
            });
            DeviceService.getAll().then(function (data) {
                $scope.devices = data;
            });

        }

        $scope.countTasks = function (finished) {
            return _.where($scope.tasks, {finished: +finished}).length;
        };

        $scope.go = function (operator) {

            if ($state.params.operatorID == operator.ID) {
                $scope.selectOperator();
            } else {
                $state.go($state.current.name, {operatorID: operator.ID});
            }
        };

        $scope.history = function (task) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-path-logs.html',
                size: 'lg',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.task = _.clone(task, true);

                    OrderService.ongoingsLogs(task.orderID).then(function (data) {
                        $scope.logs = data;
                    });

                    $scope.getTime = function (item) {
                        var logs = _.where($scope.logs, {ongoingID: item.ongoingID});
                        var diff = item.timestamp - _.first(logs).timestamp;
                        return diff;
                    }
                }
            })

        };

        $scope.formatTime = function (timeInSeconds) {
            var seconds = pad(timeInSeconds % 60);
            var minutes = pad(Math.floor(timeInSeconds / 60) % 60);
            var hours = pad(Math.floor(timeInSeconds / 3600));

            return hours + ':' + minutes + ':' + seconds
        };

        function pad(n) {
            return (n < 10) ? ("0" + n) : n;
        }

        $scope.selectOperator = function () {
            var operatorID = $state.params.operatorID;
            $scope.currentOperatorID = operatorID;
            $scope.operator = _.findWhere($scope.operators, {ID: ~~operatorID});

            $scope.logsCtrl = OperatorService.logs($scope.operator, $scope.logsConfig);
            $scope.logsCtrl.get().then(function(data){
                $scope.stateCounters={};
                _.each($scope.filterStates,function(name){
                    $scope.stateCounters[name]=0;
                });

                _.each(data,function(item){
                    $scope.stateCounters[$scope.filterStates[item.state-1]]+=1;
                });
            });
        };

        var updateTableTimeout;
        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                $scope.logsCtrl.get();
            }, 1000);
        };

        $scope.refresh = function () {
            OperatorService.getAll(true).then(function (data) {
                $scope.operators = data;
                $scope.selectOperator();
            });
        };

        $scope.applyFilter = function (state) {
            $scope.currentFilterState = state;
        };

        $scope.stateItems = function (items, state) {
            return _.filter(items, function (item) {
                return item.state == stateMap[state];
            });
        };

        init();

    });
