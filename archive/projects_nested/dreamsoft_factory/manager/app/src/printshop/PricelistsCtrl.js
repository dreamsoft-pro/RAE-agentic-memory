angular.module('digitalprint.app')
    .controller('printshop.PricelistsCtrl', function ($scope, $filter, Notification, PsPricelistService, $modal,
                                                      FileUploader, AuthDataService, MainWidgetService, $q, $config,
                                                      DeviceService) {

        function init() {

            $scope.resetForm();

            PsPricelistService.getAll().then(function (data) {
                $scope.priceLists = data;
            });

        }

        var accessTokenName = $config.API_ACCESS_TOKEN_NAME;

        var header = {};
        header[accessTokenName] = AuthDataService.getAccessToken();

        $scope.uploader = new FileUploader({
            'headers': header,
            'autoUpload ': true,
            'queueLimit': 1
        });

        $scope.uploader.onProgressAll = function (progress) {
            $scope.uploadProgress = progress;
        };

        $scope.uploader.filters.push({
            name: 'imageFilter',
            fn: function (item, options) {
                var itemName = item.name.split('.');
                var lastItem = itemName.pop();
                var possibleExtensions = ['svg', 'png'];

                if (possibleExtensions.indexOf(lastItem) > -1) {
                    return true;
                }
                Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                return false;
            }
        });

        $scope.formatSizeUnits = function (bytes) {
            return MainWidgetService.formatSizeUnits(bytes);
        };

        $scope.removeFile = function(fileItem) {
            fileItem.remove();
        };

        $scope.resetForm = function () {
            $scope.form = {};
        };

        $scope.refresh = function () {
            PsPricelistService.getAll(true).then(function (data) {
                $scope.priceLists = data;
            });
        };

        $scope.add = function () {
            PsPricelistService.add($scope.form).then(function (data) {

                if( $scope.uploader.queue.length > 0 ) {

                    changeUrl(data.item.ID).then(function () {

                        var file = $scope.uploader.queue[0];

                        var formData = [];

                        formData.push({'priceListID': data.item.ID});
                        file.formData = formData;

                        $scope.uploader.uploadAll();
                        $scope.uploader.onCompleteItem = function(item, response) {
                            $scope.resetForm();
                            data.item.icon = response.icon;
                            $scope.priceLists.push(data.item);
                            Notification.success($filter('translate')('success'));
                        };
                    });
                } else {
                    $scope.resetForm();
                    $scope.priceLists.push(data.item);
                    Notification.success($filter('translate')('success'));
                }

            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        function changeUrl(priceListID) {

            var def = $q.defer();

            _.each($scope.uploader.queue, function(item, index) {
                item.url = PsPricelistService.getUploadUrl(priceListID);

                if( index === $scope.uploader.queue.length-1 ) {
                    def.resolve(true);
                }
            });

            return def.promise;
        }

        $scope.edit = function (item) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/edit-pricelist.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.form = item;

                    $scope.save = function () {
                        PsPricelistService.edit($scope.form).then(function (data) {
                            item = data.item;
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });

                    };

                    $scope.uploadIcon = function (priceList) {
                        $modal.open({
                            templateUrl: 'src/contents/templates/modalboxes/icon-uploader.html',
                            scope: $scope,
                            backdrop: 'static',
                            keyboard: false,
                            controller: function ($scope, $modalInstance) {

                                var header = {};
                                header[accessTokenName] = AuthDataService.getAccessToken();

                                var uploader = $scope.uploader = new FileUploader({
                                    'url': PsPricelistService.getUploadUrl(),
                                    queueLimit: 1,
                                    headers: header,
                                    'autoUpload': false
                                });

                                uploader.filters.push({
                                    name: 'imageFilter',
                                    fn: function (item, options) {
                                        var itemName = item.name.split('.');
                                        var lastItem = itemName.pop();
                                        var possibleExtensions = ['svg', 'png'];

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

                                    formData.push({'priceListID': priceList.ID});
                                    file.formData = formData;

                                    uploader.uploadItem(file);

                                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                                        if (response.response == true) {
                                            priceList.icon = response.icon;

                                            var typeIdx = _.findIndex($scope.priceLists, {ID: priceList.ID});
                                            if (typeIdx > -1) {
                                                $scope.priceLists[typeIdx].icon = response.icon;
                                            }
                                            Notification.success($filter('translate')('file_uploaded'));
                                            $modalInstance.close();
                                        } else {
                                            Notification.success($filter('translate')('uploading_problem'));
                                        }
                                    };
                                };

                                $scope.cancel = function () {
                                    if (uploader.isUploading) {
                                        alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                                    } else {
                                        $modalInstance.close();
                                    }
                                }
                            }
                        });
                    };

                    $scope.deleteIcon = function (priceList) {

                        PsPricelistService.deleteIcon(priceList.ID).then(function (data) {
                            if (data.response) {
                                priceList.icon = null;
                                var typeIdx = _.findIndex($scope.priceLists, {ID: priceList.ID});
                                if (typeIdx > -1) {
                                    $scope.priceLists[typeIdx].icon = null;
                                    Notification.success($filter('translate')('deleted_successful'));
                                }
                            }
                        });

                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            })
        };

        $scope.devices = function (pricelist) {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/devices-selector.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.selectorTitle = $filter('translate')('pricelist') + ' ' + pricelist.name;
                    $scope.currentDevices = [];
                    DeviceService.getAll().then(function (data) {
                        $scope.currentDevices = _.clone(data, true);
                        PsPricelistService.devices(pricelist).then(function (data) {
                            _.each(data, function (item) {
                                var idx = _.findIndex($scope.currentDevices, {ID: item.deviceID});
                                if (idx > -1) {
                                    $scope.currentDevices[idx].selected = 1;
                                }
                            })
                        })
                    });

                    $scope.ok = function () {
                        var selectedDevices = [];
                        _.each($scope.currentDevices, function (each) {
                            if (each.selected === 1) {
                                selectedDevices.push(each.ID);
                            }
                        });

                        PsPricelistService.setDevices(pricelist, selectedDevices).then(function (data) {
                            $modalInstance.close();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.remove = function (item) {
            PsPricelistService.remove(item).then(function (data) {
                $scope.priceLists = data;
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        init();

    });
