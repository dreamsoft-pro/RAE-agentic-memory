angular.module('digitalprint.app')
    .controller('shop.SpecialAccountsCtrl', function ($scope, ApiCollection, $modal, $filter, UserService,
                                                      UserTypeService, Notification, $timeout) {

        UserTypeService.getAll().then(function (data) {
            $scope.userTypes = data;
        });

        $scope.showRows = 25;
        $scope.usersConfig = {
            count: 'users/specialCount',
            params: {
                limit: $scope.showRows,
                special: 1
            },
            onSuccess: function (data) {
                $scope.usersCtrl.items = data;
            }
        };

        $scope.usersCtrl = new ApiCollection('users/special', $scope.usersConfig);
        $scope.usersCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.usersCtrl.get();
            }, 1000);
        };


        $scope.editUser = function (user) {

            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-special-account.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {
                    $scope.user = user;
                    $scope.form = _.clone(user, true);
                    $scope.form.pass = null;

                    $scope.ok = function () {
                        UserService.editUser($scope.form).then(function (data) {
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

        $scope.editType = function (user) {

            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-special-account-type.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

                    console.log(user);
                    $scope.user = user;
                    $scope.form = {};
                    $scope.form.userTypeID = user.userTypeID;


                    $scope.ok = function () {
                        console.log($scope.form);
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

        $scope.add = function () {

            $scope.form.special = 1;

            UserService.addSpecial($scope.form).then(function (data) {
                $scope.form = {};
                $scope.usersCtrl.clearCache();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.removeUser = function (user) {

            UserService.remove(user.ID).then(function (data) {
                var idx = _.findIndex($scope.usersCtrl.items, {ID: user.ID});
                if (idx > -1) {
                    $scope.usersCtrl.items.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

    });