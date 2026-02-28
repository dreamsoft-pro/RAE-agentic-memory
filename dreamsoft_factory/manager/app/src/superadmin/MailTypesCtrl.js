angular.module('digitalprint.app')
    .controller('superadmin.MailTypesCtrl', function ($scope, $rootScope, $filter, $modal, MailTypeService, Notification) {

        $scope.form = {};

        MailTypeService.getAll().then(function (data) {
            $scope.mailTypes = data;
        }, function (data) {
            Notification.error($filter('translate')('error'));
        });

        $scope.add = function () {
            MailTypeService.create($scope.form).then(function (data) {
                $scope.mailTypes.push(data);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.edit = function (item) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/edit-mailtype.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(item, true);
                    $scope.save = function () {
                        MailTypeService.update($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.mailTypes, {
                                ID: item.ID
                            });
                            if (idx > -1) {
                                $scope.mailTypes[idx] = _.clone($scope.form, true);
                            }
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            })
        };

        $scope.variables = function (mailType) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/mail-variables.html',
                scope: $scope,
                resolve: {
                    getVariables: function () {
                        return MailTypeService.getVariables(mailType.ID).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'))
                        });
                    }
                },

                controller: function ($scope, $modalInstance, getVariables) {
                    $scope.mailType = _.clone(mailType, true);
                    $scope.variables = _.clone(getVariables, true);


                    $scope.add = function () {
                        $scope.mailTypeID = mailType.ID;

                        MailTypeService.variables($scope.mailTypeID, $scope.form).then(function (data) {
                            console.log(data);
                            $scope.variables.push(data.item);
                            $scope.form = {};
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.remove = function (variable) {
                        MailTypeService.removeVariable(mailType.ID, variable.ID).then(function (data) {
                            var idx = _.findIndex($scope.variables, {ID: variable.ID});
                            $scope.variables.splice(idx, 1);

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.edit = function (variable) {
                        $modal.open({
                            templateUrl: 'src/superadmin/templates/modalboxes/edit-variable.html',
                            scope: $scope,
                            controller: function ($scope, $modalInstance) {
                                $scope.variable = variable;
                                $scope.form = _.clone(variable, true);
                                $scope.form.mailTypeID = mailType.ID;

                                $scope.save = function () {
                                    MailTypeService.editVariable(mailType.ID, $scope.form).then(function (data) {
                                        variable = _.extend(variable, $scope.form);
                                        $modalInstance.close();
                                        Notification.success($filter('translate')('success'));
                                    }, function (data) {
                                        Notification.error($filter('translate')('error'));
                                    });
                                }
                            }
                        })
                    }
                }
            })
        };

        $scope.remove = function (item) {
            MailTypeService.remove(item.ID).then(function (data) {
                var idx = _.findIndex($scope.mailTypes, {
                    ID: item.ID
                });
                if (idx > -1) {
                    $scope.mailTypes.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            })
        }

    });