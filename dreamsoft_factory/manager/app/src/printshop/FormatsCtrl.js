'use strict';

angular.module('digitalprint.app')
    .controller('printshop.FormatsCtrl', function ($rootScope, $scope, $stateParams, $filter, PsPreflightFolderService,
                                                   Notification, $modal, PsFormatService, PsPrintTypeService, getData,
                                                   PsPrintTypeWorkspaceService, $q, $config, AuthDataService, $window) {
        var currentGroupID;
        var currentTypeID;

        $scope.formats = [];
        currentGroupID = $scope.currentGroupID = $stateParams.groupID;
        currentTypeID = $scope.currentTypeID = $stateParams.typeID;
        $scope.sortChange = false;
        $scope.form = {
            unit: 1
        };

        $scope.accessTokenName = $config.ACCESS_TOKEN_NAME;

        $rootScope.currentTypeName = getData.type.name;
        $rootScope.currentGroupName = getData.group.name;

        $scope.unitsList = [
            {'unit': 'mm', 'ID': 1},
            {'unit': 'cm', 'ID': 2}
        ];

        $scope.bindingTypes='sewn glue spiral none'.split(' ');

        var FormatService = new PsFormatService(currentGroupID, currentTypeID);

        function getAll() {
            FormatService.getAll().then(function (data) {
                $scope.formats = data;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }
        getAll();
        $scope.sortableOptions = {
            stop: function (e, ui) {
                $scope.sortChange = true;
            },
            axis: 'y',
            placeholder: 'success',
            handle: 'button.button-sort',
            cancel: ''
        };


        $scope.refreshFormats = function () {
            FormatService.getAll(true);
        };

        $scope.addFormat = function () {

            FormatService.add($scope.form).then(function (data) {
                $scope.formats.push(data);
                $scope.form = {};
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.editFormat = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-format.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = {};
                    $scope.form = angular.copy(elem);

                    $scope.save = function () {

                        FormatService.edit($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.formats, {ID: $scope.form.ID});
                            if (idx > -1) {
                                $scope.formats[idx] = angular.copy($scope.form);
                            }
                            $modalInstance.close();
                            getAll();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        };

        $scope.formatPrintTypesStart = function (elem) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/format-print-types.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.oryg = elem;
                    $scope.form = {};
                    $scope.form = angular.copy(elem);

                    $scope.printTypes = [];
                    PsPrintTypeService.getAll().then(function (data) {
                        $scope.printTypes = data;

                        _.each($scope.printTypes, function (item) {
                            var findResult = _.findWhere(elem.printTypes, {printTypeID: item.ID});
                            if (findResult) {
                                item.selected = 1;
                                item.minVolume = findResult.minVolume;
                                item.maxVolume = findResult.maxVolume;
                                item.printTypeWorkspaceExist = findResult.printTypeWorkspaceExist;

                            } else {
                                item.selected = 0;
                                item.minVolume = null;
                                item.maxVolume = null;
                                item.printTypeWorkspaceExist = false;
                            }

                        });

                    }, function (data) {
                        Notification.error($filter('translate')('error'));
                        $modalInstance.close();
                    });

                    $scope.save = function () {

                        $scope.form.printTypes = [];

                        _.each($scope.printTypes, function (item) {
                            if (item.selected === 1) {
                                $scope.form.printTypes.push({
                                    printTypeID: item.ID,
                                    minVolume: item.minVolume || null,
                                    maxVolume: item.maxVolume || null,
                                    printTypeWorkspaceExist: item.printTypeWorkspaceExist || null
                                });
                            }
                        });

                        FormatService.setPrintTypes($scope.form).then(function (data) {
                            var idx = _.findIndex($scope.formats, {ID: $scope.form.ID});

                            if (idx > -1) {
                                $scope.formats[idx].printTypes = angular.copy($scope.form.printTypes);
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            })
        };

        $scope.formatWorkspacesStart = function(element, printType) {

            $scope.oryg = element;

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/format-print-type-workspaces.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    workspaces: function () {
                        return PsPrintTypeWorkspaceService.getAll(printType.ID, element.ID).then(function (data) {
                            return data;
                        }, function (data) {
                            Notification.error($filter('translate')('data'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, workspaces) {

                    $scope.workspaces = workspaces;

                    $scope.save = function() {

                        $scope.form.printTypeID = printType.ID;
                        $scope.form.formatID = element.ID;
                        $scope.form.workspaces = [];

                        _.each($scope.workspaces, function (item) {

                            if( item.usePerSheet || item.operationDuplication ) {
                                $scope.form.workspaces.push({
                                    workspaceID: item.ID,
                                    usePerSheet: item.usePerSheet || null,
                                    operationDuplication: item.operationDuplication || null
                                });
                            }

                        });

                        FormatService.setPrintTypeWorkspaces($scope.form).then(function (data) {
                            $modalInstance.close();
                            var idx = _.findIndex(element.printTypes, {printTypeID: printType.ID});

                            if( data.savedCounter ) {
                                if( idx > -1 ) {
                                    element.printTypes[idx].printTypeWorkspaceExist = true;
                                }
                                printType.printTypeWorkspaceExist = true;
                            } else {
                                if( idx > -1 ) {
                                    element.printTypes[idx].printTypeWorkspaceExist = false;
                                }
                                printType.printTypeWorkspaceExist = false;
                            }
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }

                }
            });
        };

        $scope.removeFormat = function (elem) {

            FormatService.remove(elem).then(function (data) {
                var idx = _.findIndex($scope.formats, {ID: elem.ID});
                if (idx > -1) {
                    $scope.formats.splice(idx, 1);
                }
                Notification.success($filter('translate')('deleted_successful') + " " + elem.name);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.sortCancel = function () {
            $scope.refreshFormats();
            $scope.sortChange = false;
        };

        $scope.sortSave = function () {
            var result = [];
            _.each($scope.formats, function (item) {
                result.push(item.ID);
            });

            FormatService.sort(result).then(function (data) {
                $scope.sortChange = false;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
                $scope.sortCancel();
            });
        };


        $scope.formatPreflightFolderStart = function (format) {
            var PreflightFolder = new PsPreflightFolderService(format.ID);

            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/format-preflights.html',
                scope: $scope,
                size: 'lg',

                resolve: {
                    preflightFolders: function ($q) {
                        return PreflightFolder.getAll().then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, preflightFolders) {

                    $scope.format = format;
                    $scope.preflightFolders = _.clone(preflightFolders, true);
                    $scope.form = {};

                    $scope.add = function () {
                        PreflightFolder.add($scope.form).then(function (item) {
                            $scope.preflightFolders.push(item);
                            $scope.form = {};
                        }, function (data) {
                            console.log(data);
                        });
                    };

                    $scope.edit = function (preflightFolder) {
                        $modal.open({
                            templateUrl: 'src/printshop/templates/modalboxes/edit-preflight.html',
                            scope: $scope,

                            controller: function ($scope, $modalInstance) {

                                $scope.preflightFolder = preflightFolder;
                                $scope.form = _.clone(preflightFolder, true);

                                $scope.save = function () {
                                    PreflightFolder.edit($scope.form).then(function (data) {
                                        var idx = _.findIndex($scope.preflightFolders, {ID: $scope.form.ID});
                                        if (idx > -1) {
                                            $scope.preflightFolders[idx] = angular.copy($scope.form);
                                        }
                                        $modalInstance.close();
                                    })

                                }
                            }
                        })
                    };

                    $scope.remove = function (preflightFolder) {
                        PreflightFolder.remove(preflightFolder).then(function (data) {
                            var idx = _.findIndex($scope.preflightFolders, {ID: preflightFolder.ID});
                            if (idx > -1) {
                                $scope.preflightFolders.splice(idx, 1);
                            }
                        });
                    }

                }

            })

        };

        $scope.hasEditor = function() {
            return getData.type.isEditor === 1;

        };

        $scope.openAdminEditor = function (format) {

            var actionUrl = $config.EDITOR_URL + '?typeID=' + getData.type.ID + '&formatID=' + format.ID + '&access-token=' + AuthDataService.getAccessToken();
            $window.open(actionUrl, '_blank');

        };

        $scope.changeUnit = function() {
            changeUnit(this, 'width');
            changeUnit(this, 'height');
            changeUnit(this, 'maxHeight');
            changeUnit(this, 'maxWidth');
            changeUnit(this, 'minHeight');
            changeUnit(this, 'minWidth');
            changeUnit(this, 'slope');
        };

        function changeUnit(_this, field) {
            if( _this.form.unit === 1 ) {
                if( typeof _this.form[field] === 'string' ) {
                    _this.form[field] = parseFloat(_this.form[field].replace(',', '.')).toFixed(1);
                }
                if( _this.form[field] > 0 ) {
                    _this.form[field] *= 10;
                }
            } else if ( _this.form.unit === 2 ) {
                if( typeof _this.form[field] === 'string' ) {
                    _this.form[field] = parseFloat(_this.form[field].replace(',', '.')).toFixed(0);
                } else if( typeof _this.form[field] === 'number' ) {
                    _this.form[field] = _this.form[field].toFixed(0);
                }
                if( _this.form[field] > 0 ) {
                    _this.form[field] /= 10;
                }
            }
        }

        function addActionAttribute(url, element) {
            var def = $q.defer();

            element.setAttribute("action", url);
            def.resolve(element);

            return def.promise;
        }

        $scope.syncSize = function (form, sourceField) {
            if(sourceField==='slope'){
                $scope.syncSize(form,'width');
                $scope.syncSize(form,'netWidth');
                $scope.syncSize(form,'height');
                $scope.syncSize(form,'netHeight');
                return
            }
            var slope = form.slope ? Number(form.slope) : 0;
            var slopeTwoSides = slope * 2;
            if (sourceField === 'width') {
                form.netWidth = Number(form.width) - slopeTwoSides
            } else if (sourceField === 'netWidth') {
                form.width = Number(form.netWidth) + slopeTwoSides
            } else if (sourceField === 'height') {
                form.netHeight = Number(form.height) - slopeTwoSides
            } else if (sourceField === 'netHeight') {
                form.height = Number(form.netHeight) + slopeTwoSides
            }
            $scope.form = Object.assign($scope.form, $scope.form)
        }

    });
