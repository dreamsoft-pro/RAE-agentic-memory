angular.module('digitalprint.app')
    .controller('shop.PermissionsCtrl', function ($scope, $q, $filter, $modal, ApiCollection, UserService, $timeout,
                                                  UserTypeService, GroupService, RoleService) {


        $scope.showRows = 25;
        $scope.usersConfig = {
            count: 'users/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.usersCtrl.items = data;
            }
        };
        $scope.userTypes = [];
        $scope.groups = [];
        $scope.roles = [];

        $scope.usersCtrl = new ApiCollection('users', $scope.usersConfig);
        $scope.usersCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.usersCtrl.get();
            }, 1000);
        };

        function init() {
            UserTypeService.getAll().then(function (data) {
                $scope.userTypes = data;

                $scope.userTypes.perPage = 10;
                $scope.userTypes.currentPage = 1;
            });

            GroupService.getAll().then(function (data) {
                $scope.groups = data;

                $scope.groups.perPage = 10;
                $scope.groups.currentPage = 1;
            });

            RoleService.getAll().then(function (data) {
                $scope.roles = data;
            });
        }

        init();

        $scope.userEditType = function (user) {

            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-special-account-type.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

                    $scope.user = user;
                    $scope.form = {};
                    $scope.form.userTypeID = user.userTypeID;


                    $scope.ok = function () {

                        UserService.editUserOptionType(user, $scope.form).then(function (data) {
                            user = _.extend(user, $scope.form);
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    }
                }
            });
        };

        $scope.userRoles = function (user) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/userRoles.html',
                scope: $scope,
                resolve: {
                    getRoles: function () {
                        var def = $q.defer();
                        UserService.getRoles(user).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                            def.reject(data);
                        });

                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, getRoles) {
                    $scope.currentRoles = _.clone($scope.roles, true);
                    $scope.user = user;

                    _.each(getRoles, function (item) {
                        var findItem = _.findWhere($scope.currentRoles, {
                            ID: item
                        });
                        if (findItem) {
                            findItem.selected = 1;
                        }
                    });

                    $scope.save = function () {
                        var selectedRoles = [];
                        _.each($scope.currentRoles, function (item) {
                            if (item.selected) {
                                selectedRoles.push(item.ID);
                            }
                        });

                        UserService.setRoles(user, selectedRoles).then(function (data) {
                            Notification.success("Ok");
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error("Error");
                            console.log(data);
                        });
                    };

                }
            })
        };

        $scope.userGroups = function (user) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/userGroups.html',
                scope: $scope,
                resolve: {
                    getGroups: function () {
                        var def = $q.defer();
                        UserService.getGroups(user).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error("Error with getGroups");
                            def.reject(data);
                        });

                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, getGroups) {
                    $scope.currentGroups = _.clone($scope.groups, true);
                    $scope.user = user;

                    _.each(getGroups, function (item) {
                        var findItem = _.findWhere($scope.currentGroups, {
                            ID: item
                        });
                        if (findItem) {
                            findItem.selected = 1;
                        }
                    });

                    $scope.save = function () {
                        var selectedGroups = [];
                        _.each($scope.currentGroups, function (item) {
                            if (item.selected) {
                                selectedGroups.push(item.ID);
                            }
                        });


                        UserService.setGroups(user, selectedGroups).then(function (data) {
                            Notification.success("Ok");
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error("Error");
                            console.log(data);
                        });

                    }

                }
            })
        };



    });