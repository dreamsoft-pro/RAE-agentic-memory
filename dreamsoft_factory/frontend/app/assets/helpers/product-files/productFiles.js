angular.module('dpClient.helpers')
    .directive('productFiles', [
        function () {
            return {
                restrict: 'E',
                replace: true,
                templateUrl: 'src/cart/templates/product-files-common.html',
                controller: function ($scope, TemplateRootService, $modal, CommonService, FileUploader,
                                      $rootScope, $filter, Notification, ProductFileService, MainWidgetService) {

                    $scope.isAllowDivideText = (product, filesVolume) => {
                        return product.allowVolumeDivide && filesVolume != product.volume && $scope.isMoreFiles(product)
                    }

                    $scope.isMoreFiles=(product)=>{
                        let fileOverOne = false
                        _.each(product.fileList, (attrFile) => {
                            if (attrFile.files.length > 1) {
                                fileOverOne = true
                            }
                        })
                        return fileOverOne
                    }

                    $scope.uploadFiles = function (productID, attrID, product, volume) {
                        if ($scope.product.allowVolumeDivide && $scope.isMoreFiles(product) && !volume) {
                            Notification.warning($filter('translate')('select_volume_to_divide_warning'))
                            return
                        }

                        TemplateRootService.getTemplateUrl(34).then(function (response) {
                            $modal.open({
                                templateUrl: response.url,
                                scope: $scope,
                                backdrop: true,
                                keyboard: false,
                                size: 'lg',
                                resolve: {
                                    allowedExtensions: function () {
                                        return CommonService.getAll().then(function (data) {
                                            var extensions = [];
                                            _.each(data, function (item) {
                                                extensions.push(item['extension']);
                                            });

                                            return extensions;

                                        });
                                    }
                                },
                                controller: function ($scope, $modalInstance, allowedExtensions, $config, AuthDataService) {

                                    var accessTokenName = $config.ACCESS_TOKEN_NAME;

                                    var header = {};
                                    header[accessTokenName] = AuthDataService.getAccessToken();
                                    header.volume = volume ?? 0;

                                    var uploader = $scope.uploader = new FileUploader({
                                        'url': ProductFileService.getUploadUrl(productID, attrID),
                                        'headers': header
                                    });

                                    uploader.filters.push({
                                        name: 'imageFilter',
                                        fn: function (item, options) {
                                            var itemName = item.name.split('.');
                                            var lastItem = itemName.pop().toLowerCase();

                                            if (allowedExtensions.indexOf(lastItem) > -1) {
                                                return true;
                                            }
                                            Notification.warning($filter('translate')('required_ext') + allowedExtensions.join(', '));
                                            return false;
                                        }
                                    });

                                    uploader.onAfterAddingAll = function (addedItems) {
                                        uploader.uploadAll();
                                    };

                                    uploader.onSuccessItem = function (fileItem, response, status) {
                                        if (response.response) {
                                            Notification.info($filter('translate')('file_successfully_uploaded'))
                                            $rootScope.$emit('productFileChanged', true);
                                        } else {
                                            Notification.error($filter('translate')('error'))
                                        }

                                    };

                                    uploader.onCompleteAll = function () {
                                        $modalInstance.close();
                                    };

                                    $scope.cancel = function () {
                                        if (uploader.isUploading) {
                                            alert($filter('translate')('uploading_in_progress'));
                                        } else {
                                            $modalInstance.close();
                                        }
                                    }
                                }
                            });
                        });
                    };

                    $scope.saveProductProps = (product) => {
                        ProductFileService.saveProductProps(product.productID, product.sendToFix)
                            .then((result) => {
                                if (result) {
                                    Notification.info($filter('translate')('send_to_fix_saved'))
                                    $rootScope.$emit('productFileChanged', true);
                                } else {
                                    Notification.error($filter('translate')('error_not_saved'))
                                }
                            })
                    }

                    $scope.dimensionsValid = (file, product, level) => {
                        if (level === 'net') {
                            return product.calcProducts[0].formatWidth == (file.widthNet + product.calcProducts[0].slope * 2) && product.calcProducts[0].formatHeight == (file.heightNet + product.calcProducts[0].slope * 2)
                        } else if (level === 'gross') {
                            return product.calcProducts[0].formatWidth == file.width && product.calcProducts[0].formatHeight == file.height
                        }
                    }

                    $scope.acceptFile = (productID, fileID) => {
                        ProductFileService.acceptFile(productID, fileID).then((result) => {
                            if (result.response) {
                                Notification.info($filter('translate')('product_file_accepted'))
                                $rootScope.$emit('productFileChanged', true);
                            }
                        })
                    }

                    $scope.removeFile = function (productID, fileID) {

                        ProductFileService.removeFile(productID, fileID).then(function (response) {
                            if (response.response) {

                                Notification.info($filter('translate')('removed') + ' ' + response.removed_item.name);

                                $rootScope.$emit('productFileChanged', true);

                            } else {
                                Notification.error($filter('translate')('error'))
                            }

                        });

                    };

                    $scope.fixFileDimensions = (productID, fileID) => {
                        ProductFileService.fixFileDimensions(productID, fileID).then((result) => {
                            if (result.response) {
                                Notification.info($filter('translate')('file_dimension_fixed'))
                                $rootScope.$emit('productFileChanged', true);
                            }
                        })
                    }

                    $scope.selectFileTarget = (product, file) => {
                        ProductFileService.saveFileProps(product.ID, file.ID, {backSideTarget: file.backSideTarget}).then(result => {
                            if (result) {
                                Notification.info($filter('translate')('saved'));
                                $rootScope.$emit('productFileChanged', true);
                            } else {
                                Notification.error($filter('translate')('error'))
                            }
                        })
                    }

                    $scope.isSideAssign = (attrData, file, product) => {
                        if (product.calcProducts[0].pages > 2) {
                            return false;
                        }
                        if (attrData.doubleSidedSheet === 1) {
                            return true;
                        }
                        for (var i = 0; i < product.fileList.length; i++) {
                            if (attrData.doubleSidedSheet === 1 && attrData.attrID == 1) {
                                return true;
                            }
                        }
                        return false
                    }

                    $scope.formatSizeUnits = (bytes) => MainWidgetService.formatSizeUnits(bytes);

                    $scope.updateVolumeNumber = (product) => {
                        $scope.filesVolume = _.reduce(product.fileList, (allAttrVolume, attrFileData) => {
                            return _.reduce(attrFileData.files, (allFile, file) => {
                                return allFile + (file.volume ?? 0)
                            }, allAttrVolume)
                        }, 0);
                    }

                    $scope.checkMultivolume = (file, product) => {
                        if (!product) {
                            return
                        }
                        ProductFileService.saveFileProps(product.ID, file.ID, {volume: file.volume})
                            .then(result => {
                                if (!result) {
                                    Notification.error($filter('translate')('error'))
                                }
                            })
                        $scope.updateVolumeNumber(product);
                    }

                }
            };
        }]);
