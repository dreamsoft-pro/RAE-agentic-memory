angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionIncreasesCtrl', function ($scope, $filter, $q, $modal, $rootScope, getData, Notification,
                                                                 PsConfigOptionService, PsPricelistService,
                                                                 PsPrintTypeService, PsWorkspaceService,
                                                                 PsConfigIncreaseTypeService) {

        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;

        var ConfigOptionService;

        $scope.option = angular.copy(getData.option);
        $scope.attribute = angular.copy(getData.attribute);
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;
        function init() {
            var ControllerService = PsConfigOptionService.getControllerService($scope.attribute.type);

            ConfigOptionService = new PsConfigOptionService(currentAttrID);

            ControllerService.getAll().then(function (data) {
                $scope.controllers = data;
            });

            $scope.countIncreases = [];
            ConfigOptionService.countIncreases(currentOptID).then(function (data) {
                $scope.countIncreases = data;
            });

            PsConfigIncreaseTypeService.getAll().then(function (data) {
                $scope.increaseTypes = data;
            });
            if($scope.attribute.type==3){
                $scope.getPaperIncreases();
            }
        }

        $scope.getCountIncreases = function (controller) {
            if (!$scope.countIncreases.length) {
                return 0;
            }
            var item = _.findWhere($scope.countIncreases, {controllerID: controller.ID});
            return item ? item.count : 0;
        };

        $scope.getIncreases = function (controller) {
            $scope.increaseController = controller;

            ConfigOptionService.getIncreases(currentOptID, controller.ID).then(function (data) {
                $scope.increaselist = data;
                $scope.resetAddIncreaseForm();
            });

        };

        $scope.refreshPaperIncreases = function () {
            $scope.getPaperIncreases();
        };

        $scope.getPaperIncreases = function () {
            ConfigOptionService.getPaperIncreases(currentOptID).then(function (data) {
                $scope.increasepaperlist = data;
            });
        };

        $scope.resetAddIncreaseForm = function () {
            $scope.addIncrease = {};
            $scope.addIncrease.increaseType = _.first($scope.increaseTypes).ID;
        };

        $scope.resetAddPaperIncreaseForm = function () {
            $scope.addPaperIncrease = {};
            $scope.addPaperIncrease.increaseType = _.first($scope.increaseTypes).ID;

        };

        $scope.resetIncreaseForm = function (form) {
            form.amount = form.value = form.expense = '';
        };

        $scope.savePaperIncrease = function (item) {
            ConfigOptionService.saveIncreases(currentOptID, 0, item)
                .then(function (data) {

                    if (data.ID) {
                        var increasepaperlistExists = false;

                        _.each($scope.increasepaperlist, function (list) {
                            if (_.first(list).increaseType === data.increaseType) {
                                list.push(data);
                                $scope.resetAddPaperIncreaseForm();
                                $scope.resetIncreaseForm(item);
                                Notification.success($filter('translate')('success'));
                                increasepaperlistExists = true;
                                return false;
                            }
                        });

                        if (!increasepaperlistExists) {
                            $scope.increasepaperlist.push([data]);
                            $scope.resetAddPaperIncreaseForm();
                            $scope.resetIncreaseForm(item);
                            Notification.success($filter('translate')('success'));
                        }
                    } else if (data.info === "update" && data.item.ID) {
                        _.each($scope.increasepaperlist, function (list, i) {
                            var idx = _.findIndex(list, {
                                amount: data.item.amount,
                                increaseType: data.item.increaseType
                            });
                            if (idx > -1) {
                                list[idx] = data.item;
                                $scope.resetAddPaperIncreaseForm();
                                $scope.resetIncreaseForm(item);
                                Notification.success($filter('translate')('success'));
                                return false;
                            }

                        });
                    }
                }, function (data) {
                    console.log("Error", data);
                });
        };

        $scope.saveIncrease = function (item) {

            ConfigOptionService.saveIncreases(currentOptID, $scope.increaseController.ID, item)
                .then(function (data) {

                    if (data.ID) {
                        var increaselistExists = false;

                        _.each($scope.increaselist, function (list) {
                            if (_.first(list).increaseType === data.increaseType) {
                                list.push(data);
                                $scope.resetAddIncreaseForm();
                                $scope.resetIncreaseForm(item);
                                Notification.success($filter('translate')('success'));
                                increaselistExists = true;
                                return false;
                            }
                        });

                        if (!increaselistExists) {
                            $scope.increaselist.push([data]);
                            $scope.resetAddIncreaseForm();
                            $scope.resetIncreaseForm(item);
                            Notification.success($filter('translate')('success'));
                        }
                    } else if (data.info === "update" && data.item.ID) {
                        _.each($scope.increaselist, function (list, i) {
                            var idx = _.findIndex(list, {
                                amount: data.item.amount,
                                increaseType: data.item.increaseType
                            });

                            if (idx > -1) {
                                list[idx] = data.item;
                                $scope.resetAddIncreaseForm();
                                $scope.resetIncreaseForm(item);
                                Notification.success($filter('translate')('success'));
                                return false;
                            }

                        });
                    }
                }, function (data) {
                    console.log("Error", data);
                });

        };

        $scope.removePaperIncrease = function (item) {
            ConfigOptionService.removeIncrease(currentOptID, 0, item).then(function (data) {
                _.each($scope.increasepaperlist, function (list, i) {
                    var idx = list.indexOf(item);
                    if (idx > -1) {
                        list.splice(idx, 1);
                        if (!$scope.increasepaperlist[i].length) {
                            $scope.increasepaperlist.splice(i, 1);
                        }
                        Notification.success($filter('translate')('success'));
                        return false;
                    }

                });

            }, function (data) {
                console.log("Error", data);
            });
        };


        $scope.removeIncrease = function (item) {
            ConfigOptionService.removeIncrease(currentOptID, $scope.increaseController.ID, item).then(function (data) {
                _.each($scope.increaselist, function (list, i) {
                    var idx = list.indexOf(item);
                    if (idx > -1) {
                        list.splice(idx, 1);
                        if (!$scope.increaselist[i].length) {
                            $scope.increaselist.splice(i, 1);
                        }
                        Notification.success($filter('translate')('success'));
                        return false;
                    }

                });

            }, function (data) {
                console.log("Error", data);
            });
        };

        $scope.getIncreaseType = function (increaseTypeID) {
            return _.findWhere($scope.increaseTypes, {ID: increaseTypeID});
        };


        init();
    });
