angular.module('digitalprint.app')
    .controller('customerservice.DiscountsCtrl', function ($scope, $rootScope, $q, $filter, $modal, ModuleService,
                                                           LangSettingsRootService, Notification,
                                                           DiscountService, PromotionService, PsTypeService,
                                                           PsFormatService, $location) {

        $scope.form = {};
        $scope.discountGroups = [];
        $scope.productTypes = {};
        $scope.productFormats = {};
        $scope.discountGroupForm = {};
        $scope.promotionGroupForm = {};

        var currentDiscountGroupID = false;
        if($location.search().discountGroupId) {
            currentDiscountGroupID = parseInt($location.search().discountGroupId);
        }

        function init() {
            DiscountService.getAll().then(function (data) {
                $scope.productGroups = data.productGroups;
                $scope.discountGroups = data.discountGroups;

                if( currentDiscountGroupID ) {
                    var discountGroupIdx = _.findIndex(data.discountGroups, {ID: currentDiscountGroupID});

                    if( discountGroupIdx > -1 ) {
                        $scope.processDiscounts(data.discountGroups[discountGroupIdx]);
                    }
                }

                $scope.prodFormats = [];
                $scope.prodTypes = [];
                $scope.prodFormats2 = [];
                $scope.prodTypes2 = [];
            });
        }

        init();

        $scope.pagination = {
            perPage: 5,
            currentPage: 1
        };

        $scope.pagination.setPage = function (pageNo) {
            $scope.pagination.currentPage = pageNo;
        };

        $scope.refresh = function () {
            var domainID = $scope.currentDomain.ID;
            DiscountService.getAll().then(function (data) {
                $scope.productGroups = data.productGroups;
                $scope.discountGroups = data.discountGroups;
                $scope.prodFormats = [];
                $scope.prodTypes = [];
            });
        };

        $scope.datepicker = function () {

        };

        $scope.addDiscountGroup = function () {

            DiscountService.createGroup($scope.discountGroupForm).then(function (data) {
                if (data.response) {
                    $scope.discountGroups.push(data.item);
                    $scope.discountGroupForm = {};
                    Notification.success($filter('translate')('dg_added'));
                }
            }, function (data) {
                console.log(data);
                Notification.error("error");
            });

        };

        $scope.editDiscountGroup = function (discountGroup) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/edit-discount-groups.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = _.clone(discountGroup, true);

                    $scope.ok = function () {
                        DiscountService.updateGroup($scope.form).then(function (data) {

                            $scope.form = {};

                            if (data.response) {
                                var groupIdx = _.findIndex($scope.discountGroups, {ID: data.ID});
                                if (groupIdx > -1) {
                                    $scope.discountGroups[groupIdx].langs = data.langs;
                                }
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('updated'));
                            $scope.$parent.refresh()
                        });
                    }
                }
            });
        };

        $scope.removeDiscountGroup = function (discountGroup) {
            DiscountService.removeGroup(discountGroup.ID).then(function (data) {

                if (data.response) {
                    var groupIdx = _.findIndex($scope.discountGroups, {ID: data.item.ID});
                    if (groupIdx > -1) {
                        $scope.discountGroups.splice(groupIdx, 1);
                    }
                    Notification.success($filter('translate')('deleted_successful'));
                }

            }, function (data) {
                Notification.error(data.info);
            });
        };

        $scope.addDiscount = function (discountGroup, discount) {

            if (discount.form == undefined || discount.form.percentage == undefined) {
                Notification.warning($filter('translate')('percentage_value_of_discount_required'));
                return;
            }

            if (Number(discount.form.percentage) <= 0 || _.isNaN(Number(discount.form.percentage))) {
                Notification.warning($filter('translate')('discount_percentage_value_must_be_positive'));
                return;
            }

            if (Number(discount.form.qty_start) < 0 || Number(discount.form.qty_end) < 0) {
                Notification.warning($filter('translate')('value_can_not_be_negative'));
                return;
            }

            if (Number(discount.form.meters_start) < 0 || Number(discount.form.meters_end) < 0) {
                Notification.warning($filter('translate')('value_can_not_be_negative'));
                return;
            }

            if ((discount.form.qty_start || discount.form.qty_end) &&
                (discount.form.meters_start || discount.form.meters_end)) {
                Notification.warning($filter('translate')('discount_includes_meters_or_volumes'));
                return;
            }

            discount.form.groupID = discountGroup.ID;

            DiscountService.create(discount.form).then(function (data) {
                if (data.response) {
                    discountGroup.discounts.push(data.item);
                    discount.form = {};
                    Notification.success($filter('translate')('discount_added'));
                }
            }, function (data) {
                console.log(data);
                Notification.error(data.info);
            });

        };

        $scope.editDiscount = function (discountGroup, discount) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/edit-discounts.html',
                scope: $scope,
                resolve: {
                    getTypes: function () {
                        return $scope.getTypes;
                    },
                    getFormats: function () {
                        return $scope.getFormats;
                    }
                },
                controller: function ($scope, $modalInstance, getTypes, getFormats) {
                    $scope.form = _.clone(discount, true);
                    $scope.discountGroup = discountGroup;

                    $scope.getTypes(discountGroup, $scope.form.productGroupID);
                    $scope.getFormats(discountGroup, $scope.form.productGroupID, $scope.form.productTypeID);

                    $scope.ok = function () {

                        if (Number($scope.form.percentage) <= 0 || _.isNaN(Number($scope.form.percentage))) {
                            Notification.warning($filter('translate')('discount_percentage_value_must_be_positive'));
                            return;
                        }

                        if (Number($scope.form.qty_start) < 0 || Number($scope.form.qty_end) < 0) {
                            Notification.warning($filter('translate')('value_can_not_be_negative'));
                            return;
                        }

                        if (Number($scope.form.meters_start) < 0 || Number($scope.form.meters_end) < 0) {
                            Notification.warning($filter('translate')('value_can_not_be_negative'));
                            return;
                        }

                        if (($scope.form.qty_start || $scope.form.qty_end) &&
                            ($scope.form.meters_start || $scope.form.meters_end)) {
                            Notification.warning($filter('translate')('discount_includes_meters_or_volumes'));
                            return;
                        }

                        DiscountService.update($scope.form).then(function (data) {
                            $scope.form = {};

                            if (data.item) {
                                var groupIdx = _.findIndex($scope.discountGroups, {ID: data.item.groupID});
                                if (groupIdx > -1) {
                                    var discountIdx = _.findIndex($scope.discountGroups[groupIdx].discounts, {ID: data.item.ID});
                                    if (discountIdx > -1) {
                                        $scope.discountGroups[groupIdx].discounts[discountIdx] = data.item;
                                    }
                                }
                            }
                            $modalInstance.close();
                            Notification.success($filter('translate')('updated'));
                        });
                    }
                }
            });
        };

        $scope.removeDiscount = function (discount) {
            DiscountService.remove(discount.ID).then(function (data) {

                if (data.response) {
                    var groupIdx = _.findIndex($scope.discountGroups, {ID: data.item.groupID});
                    if (groupIdx > -1) {
                        var discountIdx = _.findIndex($scope.discountGroups[groupIdx].discounts, {ID: data.item.ID});
                        if (discountIdx > -1) {
                            $scope.discountGroups[groupIdx].discounts.splice(discountIdx, 1);
                        }
                    }
                    Notification.success($filter('translate')('deleted_successful'));
                }
            }, function (data) {
                Notification.error(data.info);
            });
        };

        $scope.getTypes = function (discountGroup, groupID) {

            PsTypeService.getAll(groupID).then(function (data) {
                $scope.productTypes[discountGroup.ID] = data;
            });

        };

        $scope.getFormats = function (discountGroup, groupID, typeID) {

            var Format = new PsFormatService(groupID, typeID);
            Format.getAll().then(function (data) {
                $scope.productFormats[discountGroup.ID] = data;
            });

        };

        $scope.processDiscounts = function(discountGroup) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/process-discounts.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    processDiscounts: function () {
                        return DiscountService.getProcessDiscounts(discountGroup.ID).then(function (data) {
                            return data;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, processDiscounts) {
                    $scope.discountGroup = discountGroup;
                    $scope.processDiscounts = processDiscounts;
                }
            });
        };

    });
