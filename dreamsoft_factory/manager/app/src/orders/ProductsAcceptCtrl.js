angular.module('digitalprint.app')
    .controller('orders.ProductsAcceptCtrl', function ($scope, $rootScope, $filter, $timeout, $modal, ApiCollection,
                                                       DpProductService, Notification, ProductFileService, $state,
                                                       FileUploader, LabelImpositionService, HelpersService) {

        $scope.HelpersService = HelpersService;
        $scope.showRows = 25;
        $scope.ordersConfig = {
            count: 'dp_products/count',
            params: {
                limit: $scope.showRows,
                accept: 0,
                production: 1
            },
            onSuccess: function (data) {
                $scope.ordersCtrl.items = data;
            }
        };

        if ($state.params.productID) {
            $scope.ordersConfig.params.ID = $state.params.productID;
        }

        $scope.ordersCtrl = new ApiCollection('dp_products', $scope.ordersConfig);
        $scope.ordersCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.ordersCtrl.clearCache();
                $scope.ordersCtrl.get();
            }, 1000);
        };

        $scope.changeFilter = function (accept) {
            $scope.ordersCtrl.params.accept = accept;
            $scope.setParams();
        };

        $scope.accept = function (order, accept) {
            accept = accept ? 1 : -1;

            if (accept === 1 && order.filesCount === 0) {
                if (!confirm($filter('translate')('accept_without_files_warning'))) {
                    return false;
                }
            }

            DpProductService.accept(order.ID, accept).then(function (data) {
                if (data.response) {
                    var idx = _.findIndex($scope.ordersCtrl.items, {ID: order.ID});
                    if (idx > -1) {
                        $scope.ordersCtrl.items.splice(idx, 1);
                    }
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')(data.info));
                }

            }, function (data) {
                console.log(data);
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.noAccept = function (product) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/production-no-accept.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.order = _.clone(product, true);
                    ProductFileService.getAll(product.ID).then(function (filesByAttr) {
                        $scope.files = _.reduce(filesByAttr, (all, attr) => {
                            return _.merge(all, _.map(attr.files, (file) => {
                                file.optName = attr.optLangs[$rootScope.currentLang.code].name
                                if (attr.files.length > 1) {
                                    file.sideTargetName = file.backSideTarget ? 'back_side' : 'front_side'
                                }
                                return file;
                            }))
                        }, []);
                        _.each($scope.files, function (item, idx) {
                            if (item.accept == 1) {
                                item.selected = 1;
                            }
                        });
                    }, function (data) {
                        Notification.error($filter('translate')('error'));
                    });

                    $scope.ok = function () {
                        var selected = [];
                        _.each($scope.files, function (item) {
                            if (!!item.selected) {
                                selected.push(item.ID);
                            }
                        });
                        DpProductService.noAccept(product.ID, $scope.rejectInfo, selected).then(function (data) {
                            var idx = _.findIndex($scope.ordersCtrl.items, {ID: product.ID});
                            if (idx > -1) {
                                $scope.ordersCtrl.items.splice(idx, 1);
                            }
                            Notification.success($filter('translate')('success'));
                            $modalInstance.close();
                        }, function (data) {
                            console.log(data);
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.signAsNew = function (product) {
            DpProductService.accept(product.ID, 0).then(function (data) {
                Notification.success($filter('translate')('success'));
                $scope.setParams();
            }, function (data) {
                Notification.error($filter('translate')('error'));
            })
        };

        $scope.showFiles = function (product) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/product-files.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    ProductFileService.getAll(product.ID).then(function (data) {
                        $scope.files = data;
                    }, function (data) {
                        Notification.error($filter('translate')('error'));
                    });

                    $scope.uploadFile = function (attrFile) {
                        return function (input) {
                            ProductFileService.uploadFile(input.target.files[0], product.products[0].ID, attrFile.userCalcProductAttrOptionID, attrFile.ID)
                                .success(function (data) {
                                    if (!data.response) {
                                        Notification.error($filter('translate')('error'));
                                        return false;
                                    }
                                    Notification.success($filter('translate')('success'));
                                    $modalInstance.close();
                                }).error(function (data, status, headers, config) {
                                Notification.error($filter('translate')('error'));
                            })
                        }
                    }
                    $scope.addFile = function (attr) {
                        return function (input) {
                            ProductFileService.addFile(input.target.files[0], product.products[0].ID, attr.cpAttrID)
                                .success(function (data) {
                                    if (!data.response) {
                                        Notification.error($filter('translate')('error'));
                                        return false;
                                    }
                                    Notification.success($filter('translate')('success'));
                                    $modalInstance.close();
                                    $scope.setParams()
                                }).error(function (data, status, headers, config) {
                                Notification.error($filter('translate')('error'));
                            })
                        }
                    }
                }
            });

        };

        $scope.showUserAddress = function (product) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/user-address-data.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope) {
                    $scope.product = product;
                }
            });
        };

        $scope.sendReport = function (product) {

            function uploadedFilesRefresh(product) {
                $scope.uploadedFiles = [];
                DpProductService.getReportFiles(product.ID).then(function (data) {
                    $scope.uploadedFiles = data;
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                });
            }

            var dataChanged = false;

            $modal.open({
                templateUrl: 'shared/templates/modalboxes/uploader.html',
                scope: $scope,
                backdrop: 'static',
                keyboard: false,
                controller: function ($scope, $modalInstance, $filter, Notification) {
                    uploadedFilesRefresh(product);
                    $scope.uploader_name = 'report_uploader';
                    $scope.readonly = $scope.ordersCtrl.params.accept !== 0
                    var uploader = $scope.uploader = new FileUploader({
                        'url': DpProductService.getReportUploadUrl(product.ID)
                    });

                    uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item /*{File|FileLikeObject}*/, options) {
                            var type = '|' + item.type.slice(item.type.lastIndexOf('/') + 1) + '|';
                            var checkType = '|jpeg|webp|jpg|pdf|'.indexOf(type) !== -1;
                            if (!checkType) {
                                Notification.warning($filter('translate')('not_supported_type_of_file') + ' - ' + type.replace(/\|/g, ''));
                            }
                            return checkType;
                        }
                    });

                    uploader.onSuccessItem = function (fileItem, response, status, headers) {
                        if (response.response) {
                            uploadedFilesRefresh(product);
                            dataChanged = true;
                        } else {
                            Notification.error($filter('translate')('error'));
                        }
                    };

                    $scope.remove = function (file) {
                        DpProductService.removeReportFile(product.ID, file.ID).then(function (data) {
                            if (data.response) {
                                uploadedFilesRefresh(product);
                                dataChanged = true;
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.cancel = function () {
                        if (uploader.isUploading) {
                            alert('Upload trwa! Poczekaj na zakończenie uploadu lub anuluj go przed zamknięciem')
                        } else {
                            if (dataChanged) {
                                $scope.ordersCtrl.clearCache();
                                $scope.ordersCtrl.get();
                            }
                            $modalInstance.close();
                        }
                    }
                    $scope.acceptReport = function (file) {
                        ProductFileService.acceptReport(product.ID, file.ID).then(function (response) {
                            if (response.response) {
                                uploadedFilesRefresh(product);
                            } else {
                                Notification.error($filter('translate')('error'))
                            }
                        }, function (error) {
                            Notification.error($filter('translate')('error'))
                        })
                    }
                }
            });

        };

        $scope.callLabelImposition = function (product) {
            ProductFileService.getAll(product.ID).then(function (attributeFileSets) {
                attributeFileSets = attributeFileSets.filter(function (item) {
                    return item.specialFunction == null
                })
                LabelImpositionService.generate(product.labelImpositionID,
                    product.ID, product.products[0].ID,
                    _.map(attributeFileSets[0].files, (file) => file.ID),
                    product.copyToSpecialFolders === 1 ? 1 : 0)
                    .then(function (result) {
                        const fileError = _.reduce(result, (all, file) => {
                            if (file.error) {
                                Notification.error(file.error)
                                return true
                            }
                            return false
                        }, false)
                        if (!fileError) {
                            product.labelImposition = result
                            Notification.success($filter('translate')('generated'))
                        }

                    }, function (error) {
                        Notification.error($filter('translate')('error'))
                    })
            });

        }

    });
