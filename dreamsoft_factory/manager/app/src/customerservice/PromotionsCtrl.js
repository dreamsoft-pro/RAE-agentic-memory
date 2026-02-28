angular.module('digitalprint.app')
    .controller('customerservice.PromotionsCtrl', function ($scope, $rootScope, $q, $filter, $modal, ModuleService,
                                                            LangSettingsRootService, Notification,
                                                            PromotionService, PsTypeService, PsFormatService,
                                                            ApiCollection, PsGroupService, FileUploader, $config,
                                                            AuthDataService ) {


        $scope.promotionGroupForm = {};
        $scope.productTypes = {};
        $scope.productFormats = {};
        $scope.productGroups = [];
        $scope.showRows = 25;

        $scope.form = {
            durationTimeType: "1",
            timeType: "1"
        };

        $scope.timeOptions = {
            1: 'days',
            2: 'hours'
        };

        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        $scope.promotionsConfig = {
            count: 'promotions/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.promotionsCtrl.items = data;
            }
        };

        $scope.promotionsCtrl = new ApiCollection('promotions', $scope.promotionsConfig);
        $scope.promotionsCtrl.get();

        function init() {

        }

        init();

        PsGroupService.getAll().then(function (data) {
            $scope.productGroups = data;
        });

        $scope.refresh = function () {
            $scope.promotionsCtrl.clearCache();
        };

        $scope.add = function () {

            PromotionService.create($scope.form).then(function (data) {
                if (data.response) {
                    $scope.refresh();
                    $scope.form = {};
                    Notification.success($filter('translate')('saved_message'));
                } else {
                    if (data.info) {
                        Notification.error($filter('translate')(data.info));
                    } else {
                        Notification.error($filter('translate')('error'));
                    }
                }

            }, function (data) {
                if (data.info) {
                    Notification.error($filter('translate')(data.info));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            });

        };

        $scope.remove = function (promotion) {
            PromotionService.remove(promotion.ID).then(function (data) {

                if (data.response) {
                    $scope.refresh();
                    Notification.success($filter('translate')('deleted_successful'));
                }
            }, function (data) {
                Notification.error(data.info);
            });
        };

        $scope.edit = function (promotion) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/edit-promotion.html',
                scope: $scope,
                resolve: {
                    getTypes: function () {
                        return $scope.getTypes;
                    },
                    getFormats: function () {
                        return $scope.getFormats;
                    },
                    refresh: function () {
                        return $scope.refresh();
                    }
                },
                controller: function ($scope, $modalInstance) {

                    $scope.form = _.clone(promotion, true);

                    getTypes($scope.form.productGroupID).then(function( types ) {
                        $scope.productTypes = types;
                        getFormats($scope.form.productGroupID, $scope.form.productTypeID).then( function(formats) {
                            $scope.productFormats = formats;
                        });
                    });

                    $scope.getTypes = function (groupID) {

                        getTypes(groupID).then(function(types) {
                            $scope.productTypes = types;
                        });

                    };

                    $scope.getFormats = function (groupID, typeID) {

                        getFormats(groupID, typeID).then(function(formats) {
                            $scope.productFormats = formats;
                        });

                    };

                    $scope.save = function () {
                        PromotionService.update($scope.form).then(function (data) {
                            if (data.response) {
                                promotion = _.extend(promotion, data.item);
                                $scope.form = {};
                                $scope.refresh();
                                $modalInstance.close();
                                Notification.success($filter('translate')('saved_message'));
                            }
                        });
                    };

                    $scope.uploadIcon = function (promotion) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new FileUploader({
                                    'url': PromotionService.getUploadUrl(),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter',
                                    fn: function (item, options) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop();
                                        var possibleExtensions = ['jpg', 'jpeg', 'png', 'svg','webp'];

                                        if (possibleExtensions.indexOf(lastItem) > -1) {
                                            return true;
                                        }
                                        Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                                        return false;
                                    }
                                });

                                $scope.ok = function () {

                                    var file = uploader.queue[0];
                                    $scope.file = file;

                                    var formData = [];

                                    formData.push({'promotionID': promotion.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response === true) {
                                            promotion.icon = response.icon;
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.success($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        Notification.warning($filter('translate')('uploading_in_progress'));
                                    } else {
                                        $modalInstance.close();
                                    }
                                }
                            }
                        });
                    };

                    $scope.deleteIcon = function (promotion) {

                        PromotionService.deleteIcon(promotion.ID).then(function (data) {
                            if (data.response) {
                                promotion.icon = null;
                                Notification.success($filter('translate')('deleted_successful'));
                            }
                        });

                    };
                }
            });
        };

        $scope.showTimeInfo = function (promotion) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/show-promotion-time-info.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.promotion = promotion;
                }
            });
        };

        function getTypes(groupID) {

            var def = $q.defer();

            PsTypeService.getAll(groupID).then(function (data) {
                def.resolve(data);
            });

            return def.promise;
        }

        $scope.getTypes = function (groupID) {

            getTypes(groupID).then(function(types) {
                $scope.productTypes = types;
            });

        };

        function getFormats(groupID, typeID) {

            var def = $q.defer();

            var Format = new PsFormatService(groupID, typeID);
            Format.getAll().then(function (data) {
                def.resolve(data);
            });

            return def.promise;

        }

        $scope.getFormats = function (groupID, typeID) {

            getFormats(groupID, typeID).then(function(formats) {
                $scope.productFormats = formats;
            });

        };

    });