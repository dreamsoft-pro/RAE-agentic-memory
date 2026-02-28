angular.module('digitalprint.app')
    .controller('superadmin.AclCtrl', function ($scope, $q, $filter, $modal, PermissionService, RoleService,
                                                UserTypeService, GroupService, UserService, Notification,
                                                ApiCollection, $timeout) {

        $scope.permissions;
        $scope.permPagination = {
            perPage: 10,
            currentPage: 1
        };
        $scope.authorizationLogs = [];

        $scope.permPagination.setPage = function (pageNo) {
            $scope.permPagination.currentPage = pageNo;
        };

        PermissionService.getAll().then(function (data) {
            $scope.permissions = data;
            $scope.filterPermissions = _.clone($scope.permissions);

        });

        $scope.addPermission = function (id) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/addPermission.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = {};
                    $scope.editMode = !_.isUndefined(id);

                    if ($scope.editMode) {
                        $scope.editItem = _.find($scope.permissions, {
                            ID: id
                        });

                        $scope.form = _.clone($scope.editItem);
                    }

                    $scope.ok = function () {

                        var done = function () {
                            $scope.form = {};
                            $scope.searchPermissions(false);
                            $modalInstance.close();
                            Notification.success("Ok");
                        };

                        if (!$scope.editMode) {
                            // PermissionService
                            PermissionService.create($scope.form).then(function (data) {
                                $scope.permissions.push(data);
                                done();
                            });
                        } else {
                            PermissionService.update($scope.form).then(function (data) {
                                $scope.editItem = _.extend($scope.editItem, $scope.form);
                                done();
                            });
                        }

                    }

                }
            });
        };

        $scope.searchPermissions = function (setFirstPage) {
            if (_.isUndefined(setFirstPage)) {
                setFirstPage = true;
            }
            $scope.filterPermissions = $filter('filter')(
                $scope.permissions,
                $scope.searchPerm
            );
            if (setFirstPage) {
                $scope.permPagination.setPage(1);
            }
        };

        $scope.removePermission = function (id) {

            var idx = _.findIndex($scope.permissions, {
                ID: id
            });

            PermissionService.remove(id).then(function () {
                $scope.permissions.splice(idx, 1);
                $scope.searchPermissions(false);
                Notification.success('Success');
            });

        };

        /**

         Roles

         **/

        $scope.roles = [];

        RoleService.getAll().then(function (data) {
            $scope.roles = data;
        });

        $scope.addRole = function (id) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/addRole.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

                    $scope.form = {};
                    $scope.editMode = !_.isUndefined(id);

                    if ($scope.editMode) {
                        $scope.editItem = _.find($scope.roles, {
                            ID: id
                        });

                        $scope.form = angular.copy($scope.editItem);
                    }

                    $scope.ok = function () {

                        var done = function () {
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success('Success');
                        };

                        if (!$scope.editMode) {
                            RoleService.create($scope.form).then(function (data) {
                                $scope.roles.push(data);
                                done();
                            });
                        } else {
                            RoleService.update($scope.form).then(function (data) {
                                $scope.editItem = _.extend($scope.editItem, $scope.form);
                                done();
                            });
                        }
                    }
                }
            });
        };

        $scope.openRoleSettings = function (id) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/roleSettings.html',
                scope: $scope,
                backdrop: 'static',
                controller: function ($scope, $modalInstance) {

                    var permissions = angular.copy($scope.permissions);
                    var currentPermissions;

                    RoleService.getRolePerms(id).then(function (data) {

                        currentPermissions = data.items;

                        $scope.rolePerms = _.groupBy(permissions, 'controller');

                    });

                    $scope.setPermission = function (perm) {

                        var indexOf = _.indexOf(currentPermissions, perm.ID);

                        if (indexOf != -1) {
                            currentPermissions.splice(indexOf, 1);
                        } else {
                            currentPermissions.push(perm.ID);
                        }

                    };

                    $scope.isActive = function (perm) {
                        return _.indexOf(currentPermissions, perm.ID) != -1;
                    };

                    $scope.ok = function () {

                        RoleService.updateSelectedRolePerms(id, currentPermissions).then(function (data) {
                            $modalInstance.close();
                        });

                    }
                }
            })
        };

        $scope.removeRole = function (role) {

            var idx = _.findIndex($scope.roles, {
                ID: role.ID
            });

            RoleService.remove(role.ID).then(function () {
                $scope.roles.splice(idx, 1);
                Notification.success('Success');
            });

        };

        /**

         Groups

         **/

        $scope.groups = [];

        GroupService.getAll().then(function (data) {
            $scope.groups = data;

            $scope.groups.perPage = 10;
            $scope.groups.currentPage = 1;
        });

        $scope.addGroup = function (id) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/addGroup.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

                    $scope.form = {};
                    $scope.editMode = !_.isUndefined(id);

                    if ($scope.editMode) {
                        $scope.editItem = _.find($scope.groups, {
                            ID: id
                        });

                        $scope.form = angular.copy($scope.editItem);
                    }

                    $scope.ok = function () {

                        var done = function () {
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success('Success');
                        };

                        if (!$scope.editMode) {
                            GroupService.create($scope.form).then(function (data) {
                                $scope.groups.push(data);
                                done();
                            });
                        } else {
                            GroupService.update($scope.form).then(function (data) {
                                $scope.editItem = _.extend($scope.editItem, $scope.form);
                                done();
                            });
                        }
                    }
                }
            });
        };

        $scope.removeGroup = function (group) {

            var idx = _.findIndex($scope.groups, {
                ID: group.ID
            });

            GroupService.remove(group.ID).then(function () {
                $scope.groups.splice(idx, 1);
                Notification.success('Success');
            });

        };

        $scope.groupRoles = function (group) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/groupRoles.html',
                scope: $scope,
                resolve: {
                    getRoles: function () {
                        var def = $q.defer();
                        GroupService.getRoles(group).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error("Errro - getGroupRoles");
                            def.reject(data);
                        });

                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, getRoles) {
                    $scope.currentRoles = _.clone($scope.roles, true);
                    $scope.group = group;

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

                        GroupService.setRoles(group, selectedRoles).then(function (data) {
                            Notification.success("Ok");
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error("Error");
                            console.log(data);
                        });

                    }

                }
            });
        };

        /**

         Users

         **/

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

        $scope.usersCtrl = new ApiCollection('users', $scope.usersConfig);
        $scope.usersCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.usersCtrl.get();
            }, 1000);
        };

        $scope.userEditType = function (user) {

            $modal.open({
                templateUrl: 'src/shop/templates/modalboxes/edit-special-account-type.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {

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
                            Notification.error("Error eith getRoles");
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

        $scope.userTypes = function (user) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/userTypes.html',
                scope: $scope,
                resolve: {
                    getTypes: function () {

                        var def = $q.defer();

                        UserService.getTypes(user).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error('error with getting user types');
                            def.reject(data);
                        });

                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, getTypes) {

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

        /**

         Types

         **/

        $scope.userTypes = [];

        UserTypeService.getAll().then(function (data) {
            $scope.userTypes = data;

            $scope.userTypes.perPage = 10;
            $scope.userTypes.currentPage = 1;
        });


        $scope.addType = function (id) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/add-type.html',
                scope: $scope,
                controller: function ($modalInstance, $scope) {
                    $scope.form = {};
                    $scope.editMode = !_.isUndefined(id);

                    if ($scope.editMode) {
                        $scope.editItem = _.find($scope.userTypes, {
                            ID: id
                        });

                        $scope.form = angular.copy($scope.editItem);
                    }

                    $scope.ok = function () {

                        var done = function () {
                            $scope.form = {};
                            $modalInstance.close();
                            Notification.success('Success');
                        };

                        if (!$scope.editMode) {
                            UserTypeService.create($scope.form).then(function (data) {
                                $scope.userTypes.push(data.item);
                                done();
                            });
                        } else {
                            UserTypeService.update($scope.form).then(function (data) {
                                _.each($scope.userTypes, function (userType) {
                                    userType['default'] = false;
                                });

                                $scope.editItem = _.extend($scope.editItem, $scope.form);
                                done();
                            });
                        }
                    }
                }
            });
        };

        $scope.typeRoles = function (type) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/typeRoles.html',
                scope: $scope,
                resolve: {
                    getRoles: function () {
                        var def = $q.defer();

                        UserTypeService.getTypeRoles(type).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            Notification.error("Errro - getGroupRoles");
                            def.reject(data);
                        });

                        return def.promise;
                    }
                },
                controller: function ($scope, $modalInstance, getRoles) {
                    $scope.currentRoles = _.clone($scope.roles, true);
                    $scope.type = type;

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

                        UserTypeService.setTypeRoles(type, selectedRoles).then(function (data) {
                            Notification.success("Ok");
                            $modalInstance.close();
                        }, function (data) {
                            Notification.error("Error");
                            console.log(data);
                        });

                    }

                }
            });
        };

        $scope.typeGroups = function (type) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/typeGroups.html',
                scope: $scope,
                resolve: {
                    getGroups: function () {
                        var def = $q.defer();
                        UserTypeService.getTypeGroups(type).then(function (data) {
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
                    $scope.type = type;

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

                        UserTypeService.setTypeGroups(type, selectedGroups).then(function (data) {
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

        $scope.removeType = function (id) {

            UserTypeService.remove(id).then(function () {
                var idx = _.findIndex($scope.userTypes, {
                    ID: id
                });
                $scope.userTypes.splice(idx, 1);
                Notification.success('Success');
            });
        };

        $scope.userAclLogs = function (user) {
            $modal.open({
                templateUrl: 'src/superadmin/templates/modalboxes/user-acl-logs.html',
                scope: $scope,
                controller: function ($scope, $modalInstance, AuthorizationLogService) {

                    var showRows = 20;

                    $scope.user = user;

                    $scope.authorizationLogsConfig = {
                        count: 'dp_authorizationLogs/count',
                        params: {
                            limit: showRows,
                            userID: user.ID
                        },
                        onSuccess: function (data) {
                            $scope.authorizationLogsCtrl.items = data;
                        }
                    };

                    $scope.setParams = function () {
                        $timeout.cancel(updateTableTimeout);
                        updateTableTimeout = $timeout(function () {
                            $scope.authorizationLogsCtrl.get();
                        }, 1000);
                    };

                    $scope.deleteByUser = function(user) {

                        AuthorizationLogService.deleteByUser(user.ID).then(function(data) {
                           if( data.response ) {
                               $scope.authorizationLogsCtrl.clearCache();
                               Notification.success($filter('translate')('deleted_successful'));
                           } else {
                               Notification.error($filter('translate')('error'));
                           }
                        });

                    };

                    $scope.authorizationLogsCtrl = new ApiCollection('dp_authorizationLogs', $scope.authorizationLogsConfig);
                    $scope.authorizationLogsCtrl.clearCache();
                }
            })
        };

    });