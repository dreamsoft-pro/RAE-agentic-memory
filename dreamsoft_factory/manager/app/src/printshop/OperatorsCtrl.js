angular.module('digitalprint.app')
    .controller('printshop.OperatorsCtrl', function ($scope, $filter, $modal, OperatorService, SkillService,
                                                     UserService, Notification, ApiCollection, $timeout) {

        $scope.userLimit = 10;

        OperatorService.getAll().then(function (data) {
            $scope.operators = data;
        });

        function init() {
            $scope.form = {};
        }

        init();

        var usersConfig = {
            params: {
                limit: $scope.userLimit
            },
            onSuccess: function (data) {
                $scope.usersCollection.items = data;
            }
        };

        $scope.usersCollection = new ApiCollection('users/searchAll', $scope.usersConfig);

        var updateTableTimeout;

        $scope.findUser = function (val, type) {
            $scope.usersCollection.params.search = val;
            $scope.usersCollection.params.type = type;
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                return $scope.usersCollection.clearCache().then(function (data) {
                    $scope.usersCollection.items = data;
                    return data;
                });
            }, 300);
            return updateTableTimeout;
        };

        $scope.userSelected = function() {
            if( $scope.form.user !== undefined ) {
                $scope.form.uID = $scope.form.user.ID;
            }

        };

        $scope.add = function () {
            OperatorService.create($scope.form).then(function (data) {
                $scope.operators.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
            });
        };

        $scope.edit = function (operator) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-operator.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.operator = _.clone(operator);
                    $scope.form = _.clone(operator);
                    $scope.ok = function () {
                        OperatorService.update($scope.form).then(function (data) {
                            $scope.form.pass = null;
                            $scope.form.pass_confirm = null;
                            operator = _.extend(operator, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error') + " " + data.info)
                        });
                    }
                }
            });
        };

        $scope.skills = function (operator) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/operator-skills.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.operator = _.clone(operator);
                    $scope.currentSkills = [];
                    SkillService.getAll().then(function (data) {
                        $scope.currentSkills = _.clone(data, true);

                        OperatorService.skills(operator).then(function (data) {
                            _.each(data, function (elem) {
                                var idx = _.findIndex($scope.currentSkills, {ID: elem});
                                if (idx > -1) {
                                    $scope.currentSkills[idx].selected = 1;
                                }
                            })
                        });
                    });

                    $scope.ok = function () {
                        var selectedSkills = [];
                        _.each($scope.currentSkills, function (each) {
                            if (each.selected === 1) {
                                selectedSkills.push(each.ID);
                            }
                        });

                        OperatorService.setSkills(operator, selectedSkills).then(function (data) {
                            console.log(data);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (id) {
            OperatorService.remove(id).then(function (data) {
                var idx = _.findIndex($scope.operators, {ID: id});
                $scope.operators.splice(idx, 1);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error') + " " + data.info)
            })
        }

        $scope.search = function () {
            var newFilter = {};
            for(var filter in $scope.filterData){
                if($scope.filterData[filter] != ''){
                    newFilter[filter] = $scope.filterData[filter];
                }
            }
            $scope.filterData = newFilter;
        };

    });