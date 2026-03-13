angular.module('digitalprint.app')
    .controller('printshop.ConfigOptionPricesCtrl', function ($rootScope, $scope, $filter, $config, $modal, localStorageService,
                                                              getData, Notification, PsConfigOptionService,
                                                              PsPriceTypeService, PsPaperPriceService, FileUploader,
                                                              DiscountService, $location, AuthDataService) {

        $scope.discountGroups = [];
        $scope.discountGroupID = null;

        var PaperPriceService;
        var ConfigOptionService;


        var currentAttrID = $scope.currentAttrID = getData.currentAttrID;
        var currentOptID = $scope.currentOptID = getData.currentOptID;
        $scope.menu = getData.menu;
        $scope.prevOption= getData.prevOption;
        $scope.nextOption= getData.nextOption;
        $rootScope.currentAttrName = getData.attribute.name;
        $rootScope.currentOptionName = getData.option.name;

        var currentControllerID = false;
        var currentDiscountGroupID = false;
        if($location.search().controllerId) {
            currentControllerID = parseInt($location.search().controllerId);
        }
        if($location.search().discountGroupId) {
            currentDiscountGroupID = parseInt($location.search().discountGroupId);
        }

        function init() {

            $scope.option = angular.copy(getData.option);
            $scope.attribute = angular.copy(getData.attribute);

            $scope.paperUnits = ['kg', 't'];

            $scope.detailPrice = {};
            var ControllerService = PsConfigOptionService.getControllerService($scope.attribute.type);

            PaperPriceService = new PsPaperPriceService(currentAttrID, currentOptID);

            ControllerService.getAll().then(function (data) {
                $rootScope.controllers = data;

                if( currentControllerID ) {
                    var currentControllerIdx = _.findIndex(data, {ID: currentControllerID});

                    if( currentControllerIdx > -1 ) {
                        $scope.getPrices(data[currentControllerIdx]);
                        if( currentDiscountGroupID ) {
                            $scope.changeDiscountGroup(currentDiscountGroupID);
                        }
                    }
                }

            });

            ConfigOptionService = new PsConfigOptionService(currentAttrID);

            $scope.countPrices = [];
            ConfigOptionService.countPrices(currentOptID).then(function (data) {
                $scope.countPrices = data;
            });

            PsPriceTypeService.getAll().then(function (data) {
                $scope.priceTypes = data;
            });

            if ($scope.attribute.type === 3) {
                $scope.paperPriceForm = {};
                $scope.getPaperPrice();
            }

            DiscountService.getGroups().then(function (discountGroups) {
                $scope.discountGroups = discountGroups;
            });

        }

        $scope.getCountPrices = function (controller) {
            if (!$scope.countPrices.length) {
                return 0;
            }
            var item = _.findWhere($scope.countPrices, {controllerID: controller.ID});
            return item ? item.count : 0;
        };

        $scope.getPrices = function (controller) {
            $scope.priceController = controller;
            $scope.discountGroupID = null;
            reloadSelectInput();

            ConfigOptionService.getDetailPrices(currentOptID, controller.ID).then(function (data) {
                $scope.detailPrice = data;
                $scope.formDetailPrice = _.clone($scope.detailPrice);
            });

            ConfigOptionService.getPrices(currentOptID, controller.ID).then(function (data) {
                $scope.pricelist = data;
                $scope.resetAddPriceForm();
                setEditPriceDiscountGroup();
            });

        };

        function reloadSelectInput() {
            $('select.discountGroupSelect').removeAttr('selected').find('option:first').attr('selected', 'selected');
        }

        $scope.changeDiscountGroup = function ( discountGroupID ) {

            if( discountGroupID === undefined ) {
                $scope.discountGroupID = this.discountGroupID;
            } else {
                $scope.discountGroupID = discountGroupID;
            }

            if (!$scope.discountGroupID) {
                ConfigOptionService.getPrices(currentOptID, $scope.priceController.ID).then(function (data) {
                    $scope.pricelist = data;
                    $scope.resetAddPriceForm();
                    setEditPriceDiscountGroup();
                });
            } else {
                ConfigOptionService.getDiscountPrices(currentOptID, $scope.priceController.ID, $scope.discountGroupID).then(function (data) {
                    _.each(data, function(prices) {
                        _.each(prices, function(price) {
                           price.discountGroupID = $scope.discountGroupID;
                        });
                    });
                    $scope.pricelist = data;
                    $scope.resetAddPriceForm();
                    setEditPriceDiscountGroup();
                });
            }
        };

        function setEditPriceDiscountGroup() {
            if( $scope.editPrice === undefined ) {
                $scope.editPrice = {};
            }
            if( $scope.discountGroupID > 0 ) {
                $scope.editPrice.discountGroupID = $scope.discountGroupID;
            } else {
                $scope.editPrice.discountGroupID = null;
            }
        }

        $scope.getPaperPrice = function () {
            PaperPriceService.getAll().then(function (data) {
                $scope.paperPrices = data;
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('data_retrieve_failed'));
            });
        };

        $scope.refreshPaperPrice = function () {
            PaperPriceService.getAll(true).then(function (data) {
                $scope.paperPrices = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });
        };

        $scope.setPaperPrice = function () {
            PaperPriceService.set($scope.paperPriceForm).then(function (data) {
                $scope.refreshPaperPrice();
                Notification.success($filter('translate')('success'));
                $scope.resetPaperPriceForm();
            }, function (data) {
                $scope.resetPaperPriceForm();
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.resetPaperPriceForm = function () {
            $scope.paperPriceForm = {};
        };

        $scope.removePaperPrice = function (item) {
            PaperPriceService.remove(item.ID).then(function (data) {
                $scope.refreshPaperPrice();
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.resetDetailPrice = function () {
            $scope.formDetailPrice = _.clone($scope.detailPrice);
        };

        $scope.saveDetailPrice = function () {

            ConfigOptionService.setDetailPrices(currentOptID, $scope.priceController.ID, $scope.formDetailPrice).then(function (data) {
                $scope.detailPrice = _.clone($scope.formDetailPrice);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                $scope.resetDetailPrice();
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.resetAddPriceForm = function () {
            $scope.addPrice = {};
            $scope.addPrice.priceType = _.first($scope.priceTypes).ID;
            if( $scope.discountGroupID > 0 ) {
                $scope.addPrice.discountGroupID = $scope.discountGroupID;
            }
        };

        // do edit
        $scope.resetPriceForm = function (form) {
            // nie resetujemy printType
            form.amount = form.value = form.expense = '';
            if( $scope.discountGroupID > 0 ) {
                form.discountGroupID = $scope.discountGroupID;
            }
        };

        $scope.savePrice = function (item) {

            if( item.discountGroupID !== item.discountGroupID ) {
                $scope.changeDiscountGroup(item.discountGroupID);
            }

            ConfigOptionService.savePrices(currentOptID, $scope.priceController.ID, item)
                .then(function (data) {
                    if (data.ID) {
                        var pricelistExists = false;

                        _.each($scope.pricelist, function (list) {
                            if (_.first(list).priceType === data.priceType) {
                                list.push(data);
                                $scope.resetAddPriceForm();
                                $scope.resetPriceForm(item);
                                Notification.success($filter('translate')('success'));
                                pricelistExists = true;
                                return false;
                            }
                        });

                        if (!pricelistExists) {
                            console.log(data);
                            $scope.pricelist.push([data]);
                            $scope.resetAddPriceForm();
                            $scope.resetPriceForm(item);
                            Notification.success($filter('translate')('success'));
                        }
                    } else if (data.info === "update" && data.item.ID) {
                        _.each($scope.pricelist, function (list, i) {
                            var idx = _.findIndex(list, {amount: data.item.amount, priceType: data.item.priceType});
                            if (idx > -1) {
                                list[idx] = data.item;
                                $scope.resetAddPriceForm();
                                $scope.resetPriceForm(item);
                                Notification.success($filter('translate')('success'));
                                return false;
                            }

                        });
                    }
                }, function (data) {
                    console.log("Error", data);
                });

        };

        $scope.removePrice = function (item) {

            if ($scope.discountGroupID > 0) {
                ConfigOptionService.removeDiscountPrice(
                    currentOptID,
                    $scope.priceController.ID,
                    item,
                    $scope.discountGroupID).then(function (data) {

                    removeFromPriceList(item);

                }, function (data) {
                    console.log("Error", data);
                });
            } else {
                ConfigOptionService.removePrice(currentOptID, $scope.priceController.ID, item).then(function (data) {

                    removeFromPriceList(item);

                }, function (data) {
                    console.log("Error", data);
                });
            }

        };

        function removeFromPriceList( item ) {
            _.each($scope.pricelist, function (list, i) {
                var idx = list.indexOf(item);
                if (idx > -1) {
                    list.splice(idx, 1);
                    if (!$scope.pricelist[i].length) {
                        $scope.pricelist.splice(i, 1);
                    }
                    Notification.success($filter('translate')('success'));
                    return false;
                }

            });
        }

        $scope.getPriceType = function (priceTypeID) {
            return _.findWhere($scope.priceTypes, {ID: priceTypeID});
        };

        $scope.importDialog = function (priceTypeID) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/option-pricelist-import.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {

                    $scope.import = {};

                    if (priceTypeID !== undefined) {
                        $scope.import.firstPriceType = _.first($scope.priceTypes, {ID: priceTypeID});
                    }

                    var uploadResource = [
                        ConfigOptionService.getResource(),
                        $scope.currentOptID,
                        'priceControllers',
                        $scope.priceController.ID,
                        'ps_prices',
                        'importPriceList'
                    ];

                    var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

                    var header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();

                    $scope.uploader = new FileUploader({
                        url: $config.API_URL + uploadResource.join('/'),
                        queueLimit: 1,
                        headers: header,
                        'autoUpload': false
                    });

                    $scope.uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item /*{File|FileLikeObject}*/, options) {
                            var itemName = item.name.split('.');
                            var lastItem = itemName.pop();
                            if (lastItem === 'csv') {
                                return true;
                            }
                            Notification.warning($filter('translate')('required_ext') + 'csv');
                            return false;
                        }
                    });

                    $scope.ok = function () {

                        if ($scope.import.priceType === undefined) {
                            Notification.warning($filter('translate')('select_print_type'));
                        }

                        var file = $scope.uploader.queue[0];

                        $scope.uploader.data = {};

                        var formData = [{
                            'priceType': $scope.import.priceType
                        }];

                        if( $scope.discountGroupID > 0 ) {
                            formData[0].discountGroupID = $scope.discountGroupID
                        }
                        file.formData = formData;

                        $scope.uploader.uploadItem(file);

                        $scope.uploader.onSuccessItem = function (item, data) {
                            if (data.response) {
                                Notification.success('Import pomyślny');
                                if( $scope.discountGroupID > 0 ) {
                                    $scope.changeDiscountGroup();
                                } else {
                                    $scope.getPrices($scope.priceController);
                                }
                                $modalInstance.close();
                            } else {
                                Notification.error("Error");
                            }
                        }
                    };

                }
            })
        };

        $scope.removeAllPrices = function (priceTypeID) {
            if( $scope.discountGroupID > 0 ) {
                ConfigOptionService.removeAllDiscountPrice($scope.currentOptID, $scope.priceController.ID, priceTypeID, $scope.discountGroupID).then(function (data) {
                    if (data.response === true) {
                        if( $scope.discountGroupID > 0 ) {
                            $scope.changeDiscountGroup();
                        } else {
                            $scope.getPrices($scope.priceController);
                        }
                        Notification.success($filter('translate')('success'));
                    }
                });
            } else {
                ConfigOptionService.removeAllPrice($scope.currentOptID, $scope.priceController.ID, priceTypeID).then(function (data) {
                    if (data.response === true) {
                        if( $scope.discountGroupID > 0 ) {
                            $scope.changeDiscountGroup();
                        } else {
                            $scope.getPrices($scope.priceController);
                        }
                        Notification.success($filter('translate')('success'));
                    }
                });
            }

        };

        $scope.showDiscountGroupName = function() {
            var index = _.findIndex($scope.discountGroups, {ID: parseInt($scope.discountGroupID)});

            if( index > -1 ) {
                return $scope.discountGroups[index].langs[$rootScope.currentLang.code].name;
            } else {
                return $filter('translate')('basic_prices');
            }

        };

        init();

    });
