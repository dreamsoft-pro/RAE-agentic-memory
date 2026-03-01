angular.module('digitalprint.app')
    .controller('contents.MailContentsCtrl', function ($scope, $stateParams, $q, $filter, $modal, MailTypeService,
                                                       MailContentService, Notification, PsGroupService, PsTypeService,
                                                       PsFormatService, CurrencyService, SettingService ) {

        $scope.showCouponForm = false;
        $scope.form = {};
        $scope.couponForm = {};
        $scope.defaultCurrency = {};
        $scope.productGroups = [];
        $scope.showTextAngular = true;

        $scope.mainProductTypes = [];
        $scope.mainProductFormats = [];

        var settings = new SettingService('registerCoupon');

        var currentTypeID = $scope.currentTypeID = parseInt($stateParams.typeID);

        var MailContent = new MailContentService(currentTypeID);

        MailTypeService.getAll().then(function (data) {
            $scope.mailTypes = data;
            $scope.mailType = _.findWhere($scope.mailTypes, {ID: currentTypeID});

            if( $scope.mailType.key === 'register' ) {
                couponSettings();
            }

        }, function (data) {
            Notification.error($filter('translate')('error'));
        });

        var convertMailData = function (data) {
            if (_.isArray(data) && !data.length) {
                $scope.form = {};
            } else {
                _.each(data, function (item, key) {
                    if (!$scope.form.titles) {
                        $scope.form.titles = {};
                    }
                    $scope.form.titles[key] = item.title;

                    if (!$scope.form.contents) {
                        $scope.form.contents = {};
                    }
                    $scope.form.contents[key] = item.content;
                });
            }
        };

        function init() {

            PsGroupService.getAll().then(function (data) {
                $scope.productGroups = data;
            });

            CurrencyService.getDefault().then( function(data) {
                $scope.defaultCurrency = data;
            });

            MailTypeService.getVariables(currentTypeID).then(function (data) {
                $scope.variables = data;
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

            MailContent.getAll().then(function (data) {
                convertMailData(data);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        }

        function couponSettings() {

            settings.getAll().then(function (data) {
                if( data.value && data.value.value > 0 ) {
                    $scope.showCouponForm = true;
                }
                if( data.groupID && data.groupID.value ) {
                    $scope.getMainTypes(data.groupID.value);
                }
                if( data.typeID && data.typeID.value ) {
                    $scope.getMainFormats(data.groupID.value, data.typeID.value);
                }
                _.merge($scope.couponForm, data);
            });

        }

        function saveRegisterCoupon() {
            settings.save($scope.couponForm).then(function (data) {
                // ok
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        }

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

        $scope.save = function () {
            var request = {};
            _.each($scope.form.titles, function (item, key) {
                if (!request[key]) {
                    request[key] = {};
                }
                request[key].title = item;
            });
            _.each($scope.form.contents, function (item, key) {
                if (!request[key]) {
                    request[key] = {};
                }
                request[key].content = item;
            });

            if( $scope.showCouponForm ) {
                saveRegisterCoupon();
            } else {
                settings.delete('value').then(function(removed) {
                    console.log(removed);
                });
            }


            MailContent.edit(request).then(function (data) {
                Notification.success($filter('translate')('success'));
            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.resetForm = function (data) {
            $scope.couponForm = {};
            MailContent.getAll(true).then(function (data) {
                convertMailData(data);
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.toggleSwitch = function( name, state ) {
            $scope.couponForm[name] = state ? 1 : 0;
        };

        $scope.showRegisterCoupon = function() {
            $scope.showCouponForm = !$scope.showCouponForm;
        };

        init();

    });