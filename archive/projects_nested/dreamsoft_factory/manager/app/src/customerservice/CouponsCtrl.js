/**
 * Created by Rafał on 20-06-2017.
 */
'use strict';
angular.module('digitalprint.app')
    .controller('customerservice.CouponsCtrl', function ($scope, $filter, Notification, $timeout, ApiCollection,
                                                         PsFormatService, PsTypeService, PsGroupService, CouponService,
                                                         CurrencyService, $modal) {

        $scope.form = {'percent': 1};
        $scope.productGroups = [];
        $scope.productTypes = {};
        $scope.productFormats = {};

        $scope.mainProductTypes = [];
        $scope.mainProductFormats = [];

        $scope.showRows = 25;

        $scope.defaultCurrency = {};

        $scope.couponsConfig = {
            count: 'dp_coupons/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function(data){
                PsGroupService.getAll().then(function (data) {
                    $scope.productGroups = data;
                });
                $scope.couponsCtrl.items = data;
            }
        };

        $scope.couponsCtrl = new ApiCollection('dp_coupons', $scope.couponsConfig);
        $scope.couponsCtrl.get();

        var updateTableTimeout;
        $scope.setParams = function() {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function(){
                $scope.couponsCtrl.get();
            }, 1000);
        };

        function resetForm() {
            $scope.form = {'percent': 1};
            $scope.form.expires = null;
        }

        function init() {
            $(".bootstrap-switch-multiUser").bootstrapSwitch();

            $(".bootstrap-switch-multiUser").on('switchChange.bootstrapSwitch', function(event, state) {
                $scope.toggleSwitch('multiUser', state);
            });

            $(".bootstrap-switch-percent").bootstrapSwitch();

            $(".bootstrap-switch-percent").on('switchChange.bootstrapSwitch', function(event, state) {
                $scope.toggleSwitch('percent', state);
            });

            CurrencyService.getDefault().then( function(data) {
                $scope.defaultCurrency = data;
            });
        }

        $scope.getTypes = function (coupon, groupID) {

            PsTypeService.getAll(groupID).then(function (data) {
                $scope.productTypes[coupon.ID] = data;
            });

        };

        $scope.getFormats = function (coupon, groupID, typeID) {

            var Format = new PsFormatService(groupID, typeID);
            Format.getAll().then(function (data) {
                $scope.productFormats[coupon.ID] = data;
            });

        };

        $scope.getMainTypes = function (groupID) {

            PsTypeService.getAll(groupID).then(function (data) {
                $scope.mainProductTypes = data;
            });

        };

        $scope.getMainFormats = function (groupID, typeID) {

            var Format = new PsFormatService(groupID, typeID);
            Format.getAll().then(function (data) {
                $scope.mainProductFormats = data;
            });

        };

        $scope.save = function() {
            CouponService.add($scope.form).then( function(data) {
                if( data.response === true) {
                    $scope.couponsCtrl.clearCache();
                    resetForm();
                    $scope.showLink(data.exportPath);
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function(reason) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.remove = function(coupon) {
            CouponService.delete(coupon.ID).then( function(data) {
                if( data.response === true) {
                    $scope.couponsCtrl.clearCache();
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function() {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.addRelation = function( coupon ) {
            var data = {};
            data.couponID = coupon.ID;
            if( coupon.form !== undefined ) {
                data.groupID = coupon.form.products.groupID;
                data.typeID = coupon.form.products.typeID;
                data.formatID = coupon.form.products.formatID;
            }

            CouponService.addProduct(data).then(function (data){
                if(data.response === true) {
                    if(data.item) {
                        var couponIndex = _.findIndex($scope.couponsCtrl.items, {ID: coupon.ID});
                        if( couponIndex > -1 ) {
                            if( $scope.couponsCtrl.items[couponIndex].products === null ) {
                                $scope.couponsCtrl.items[couponIndex].products = [];
                            }
                            $scope.couponsCtrl.items[couponIndex].products.push(data.item);
                        }
                    }
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    if( data.info === 'duplicate_all_items' ) {
                        Notification.error($filter('translate')(data.info));
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                }
            });

        };

        $scope.deleteRelation = function(coupon, couponProduct) {
            CouponService.deleteProduct(couponProduct.ID).then(function (data){
                if(data.response === true) {
                    var couponIndex = _.findIndex($scope.couponsCtrl.items, {ID: coupon.ID});
                    if( couponIndex > -1 ) {
                        var index = _.findIndex(coupon.products, {ID: couponProduct.ID});
                        if( index > -1 ) {
                            $scope.couponsCtrl.items[couponIndex].products.splice(index, 1);
                        }
                    }
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });
        };

        $scope.toggleSwitch = function( name, state ) {
            $scope.form[name] = state ? 1 : 0;
        };

        $scope.showLink = function( exportPath ) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/get-coupons.html',
                scope: $scope,
                keyboard: false,
                controller: function ($scope, $modalInstance) {

                    $scope.exportPath = exportPath;

                }
            });
        };

        init();

    });