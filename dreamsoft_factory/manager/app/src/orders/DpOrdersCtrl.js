'use strict';

angular.module('digitalprint.app')
    .controller('orders.DpOrdersCtrl', function ($scope, $timeout, $modal, ApiCollection, DpOrderService,
                                                 UserAddressService, DeliveryService, InvoiceService,
                                                 DpStatusService, $state, $filter, $config, Notification, $window,
                                                 RealizationTimeService, MainWidgetService, socket,
                                                 localStorageService, ReclamationFaultService, DpProductService,
                                                 $rootScope, FileUploader, AuthDataService, ReclamationService,
                                                 UserService, $q, OrderMessageWidgetService, CalcFileService) {

        $scope.statuses = [];
        $scope.sellers = [];

        $scope.showRows = 25;
        $scope.ordersConfig = {
            count: 'dp_orders/count',
            params: {
                production: 1,
                isOrder: 1,
                ready: 1,
                limit: $scope.showRows
            },
            onSuccess: function (orders) {
                var tmpProduct = null;
                _.each(orders, function (order, key, obj) {
                    tmpProduct = _.reduce(order.products, function (memo, num) {
                        if (!memo) {
                            return num;
                        }
                        if (MainWidgetService.compareDates(num.realisationDate, memo.realisationDate)) {
                            return num;
                        }
                        return memo;
                    });
                    if (tmpProduct) {
                        obj[key].allRealisationDate = tmpProduct.realisationDate;
                    }
                    _.each(order.products, (product) => {
                        product.filesAcceptedCount = _.filter(product.files, (file) => file.accept === 1).length;
                    })
                });

                $scope.dpOrdersCtrl.items = orders;
            }
        };

        $scope.realisationTimes = [];
        $scope.realisationColors = {
            0: '#45b6af',
            1: '#E26A6A',
            2: '#ffe567'
        };

        $scope.paymentReminderColors = {
            0: 'btn-default',
            1: 'btn-success',
            2: 'btn-warning',
            3: 'red-sunglo'
        };
        $scope.dpOrdersCtrl = new ApiCollection('dp_orders', $scope.ordersConfig);

        $scope.dpOrdersCtrl.setParam('production', 1);
        $scope.dpOrdersCtrl.setParam('isOrder', 1);
        $scope.dpOrdersCtrl.setParam('ready', 1);

        if ($state.params.orderID) {
            $scope.dpOrdersCtrl.setParam('ID', $state.params.orderID);
        }

        $scope.dpOrdersCtrl.clearCache();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.dpOrdersCtrl.get({cache: false});
            }, 1000);
        };

        $scope.setUserName = function () {
            var value = this.dpOrdersCtrl.params.userName;

            $scope.dpOrdersCtrl.setParam('name', value);
            $scope.dpOrdersCtrl.setParam('lastname', value);

            this.setParams();
        };

        $scope.setNipOrPhone = function () {
            var value = this.dpOrdersCtrl.params.nipOrPhone;

            $scope.dpOrdersCtrl.setParam('nip', value);
            $scope.dpOrdersCtrl.setParam('telephone', value);

            this.setParams();
        };

        $scope.showProducts = function (order) {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/order-products-list.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.order = order;
                }
            });
        };

        $scope.toggleValue = function (item, prop) {

            var data = {};
            data[prop] = !!!item[prop];

            DpOrderService.patch(item.ID, data).then(function (res) {
                item[prop] = data[prop];
            });
        };

        $scope.togglePaid = function (order, prop) {

            var data = {};
            data[prop] = !!!order[prop];

            DpOrderService.togglePaid(order.ID, data).then(function (res) {
                order[prop] = data[prop];
                if (order.paid === 1 && order.displayRealisationDate === 'no_payment') {
                    order.displayRealisationDate = true;
                    $scope.dpOrdersCtrl.get({cache: false});
                } else if (order.paid === 0 && order.displayRealisationDate === true) {
                    order.displayRealisationDate = 'no_payment';
                }
            });
        };

        $scope.addresses = function (order) {

            var UserAddress = new UserAddressService(order.userID);

            $modal.open({

                templateUrl: 'src/orders/templates/modalboxes/addresses.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {

                    $scope.addresses = order.addresses;
                    $scope.order = order;

                    console.log('order: ', order);

                }
            });
        };

        function init() {
            DpStatusService.getAll(1).then(function (data) {
                $scope.statuses = data;
            });
            RealizationTimeService.getAll().then(function (data) {
                _.each(data, function (one, index) {
                    if (one.color === null || one.color === '') {
                        one.color = $scope.realisationColors[index % 3];
                    }
                });
                $scope.realisationTimes = data;
            });

            socket.emit('onOrderAdminPanel', {'admin': true});

            $rootScope.$emit('Orders:unreadMessages', 0);

            socket.on('order.newMessage', function (newMessage) {
                var orderIdx = _.findIndex($scope.dpOrdersCtrl.items, {ID: newMessage.orderID});
                if (orderIdx > -1) {
                    if ($scope.dpOrdersCtrl.items[orderIdx].countMessages === undefined) {
                        $scope.dpOrdersCtrl.items[orderIdx].countMessages = 1;
                    } else {
                        $scope.dpOrdersCtrl.items[orderIdx].countMessages++;
                    }
                    if ($scope.dpOrdersCtrl.items[orderIdx].unreadMessages === undefined) {
                        $scope.dpOrdersCtrl.items[orderIdx].unreadMessages = 1;
                    } else {
                        $scope.dpOrdersCtrl.items[orderIdx].unreadMessages++;
                    }
                }
            });

            UserService.getUsersByType().then(function (data) {
                $scope.sellers = data;
            });
        }

        init();

        $scope.invoiceAddresses = function (order) {

            var UserAddressInvoice = new UserAddressService(order.userID);

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/order-invoice-data.html',
                scope: $scope,
                resolve: {

                    dpUserAddressesInvoice: function () {

                        return UserAddressInvoice.getAllAddressesVat().then(function (data) {
                            return data;
                        });
                    }

                },

                controller: function ($scope, $modalInstance, dpUserAddressesInvoice) {

                    $scope.order = order;
                    $scope.invoiceAddresses = dpUserAddressesInvoice;
                    $scope.form = {};

                    if ($scope.order.invoiceAddress) {
                        $scope.form.addressID = $scope.order.invoiceAddress.copyFromID;
                        $scope.oldAddressID = $scope.order.invoiceAddress.ID;
                    }


                    $scope.save = function () {

                        $scope.form.orderID = order.ID;
                        $scope.form.oldAddressID = $scope.oldAddressID;

                        DpOrderService.updateVatAddress($scope.form).then(function (data) {


                            if (data.response) {
                                $scope.order.invoiceAddress = _.clone(data.address, true);
                                $scope.oldAddressID = $scope.order.invoiceAddress.ID;
                            }

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }

            });
        };

        $scope.changeStatus = function (order) {

            DpOrderService.patch(order.ID, {
                status: order.status.ID
            }).then(function (data) {
                if (data.currentStatus) {
                    order.status = data.currentStatus;
                }
                if (data.changeInvoiceType) {
                    order['invoiceType'] = 2;
                }
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.getOrderInvoice = function (order) {
            InvoiceService.get(order.ID).then(function (data) {
                if (data.success === true) {
                    $window.open(data.link, '_blank');
                }
            });

            return true;
        };

        $scope.changeInvoiceType = function (order) {
            InvoiceService.changeInvoiceType(order.ID, 2).then(function (data) {
                if (data.response === true) {
                    if (data.invoiceID) {
                        order['invoiceType'] = 2;
                    }
                    Notification.success($filter('translate')('success'));
                } else {
                    Notification.error($filter('translate')('error'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.messages = function (order) {
            OrderMessageWidgetService.messagesModal($scope, order, socket, {'type': 'order'});
        };

        $scope.paymentRemind = function (order) {

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/payment-reminder.html',
                scope: $scope,
                resolve: {

                    dpPaymentsReminds: function () {
                        return DpOrderService.paymentRemind(order.ID).then(function (data) {
                            return data;
                        });
                    }

                },
                controller: function ($scope, $modalInstance, dpPaymentsReminds) {

                    $scope.paymentReminds = [];
                    $scope.currentOrderRemindCount = order.remindDatesCount;
                    if (dpPaymentsReminds.length > 0) {
                        if (dpPaymentsReminds[0].remindDate1) {
                            $scope.paymentReminds[0] = dpPaymentsReminds[0].remindDate1;
                        }
                        if (dpPaymentsReminds[0].remindDate2) {
                            $scope.paymentReminds[1] = dpPaymentsReminds[0].remindDate2;
                        }
                        if (dpPaymentsReminds[0].remindDate3) {
                            $scope.paymentReminds[2] = dpPaymentsReminds[0].remindDate3;
                        }
                    }
                    $scope.send = function () {
                        var postdata = {mailNum: order.remindDatesCount + 1};
                        DpOrderService.sendPaymentRemind(order.ID, postdata).then(function (data) {
                            if (data.send === true) {
                                $scope.paymentReminds.push(data.remindDate);
                                order.remindDatesCount++;
                                if (!order.remindDates) {
                                    order.remindDates = [];
                                }
                                order.remindDates.push(data.remindDate);
                                $scope.currentOrderRemindCount = order.remindDatesCount;
                                $modalInstance.close();
                            }
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            });
        };

        $scope.fileRemind = function (order) {

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/file-reminder.html',
                scope: $scope,
                resolve: {

                    dpFileReminds: function () {
                        return DpOrderService.fileReminder(order.ID).then(function (data) {
                            return data;
                        });
                    }

                },
                controller: function ($scope, $modalInstance, dpFileReminds) {

                    $scope.fileReminds = [];
                    $scope.currentOrderRemindCount = order.fileRemind.datesCount;
                    if (dpFileReminds.length > 0) {
                        console.log(dpFileReminds[0]);
                        if (dpFileReminds[0].remindDate1) {
                            $scope.fileReminds[0] = dpFileReminds[0].remindDate1;
                        }
                        if (dpFileReminds[0].remindDate2) {
                            $scope.fileReminds[1] = dpFileReminds[0].remindDate2;
                        }
                        if (dpFileReminds[0].remindDate3) {
                            $scope.fileReminds[2] = dpFileReminds[0].remindDate3;
                        }
                    }
                    $scope.send = function () {
                        var postData = {mailNum: order.fileRemind.datesCount + 1};
                        DpOrderService.sendFileRemind(order.ID, postData).then(function (data) {
                            if (data.send === true) {
                                $scope.fileReminds.push(data.remindData);
                                order.fileRemind.datesCount++;
                                if (!order.fileRemind.dates) {
                                    order.fileRemind.dates = [];
                                }
                                order.fileRemind.dates.push(data.remindDate);
                                $scope.currentOrderRemindCount = order.fileRemind.datesCount;
                                $modalInstance.close();
                            }
                        });
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    }
                }
            });

        };

        $scope.createReclamation = function (order) {

            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/create-reclamation.html',
                scope: $scope,
                resolve: {
                    faults: function () {
                        return ReclamationFaultService.getFaults().then(function (faults) {
                            return faults;
                        });
                    },
                    products: function () {
                        return DpProductService.getByOrder(order.ID).then(function (productData) {
                            return productData;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, faults, products) {

                    $scope.faults = faults;
                    $scope.products = products;
                    $scope.order = order;
                    $scope.showNormalPrices = true;
                    $scope.showPercentPrices = true;


                    $scope.form = {};
                    $scope.form.faults = {};
                    _.each(faults, function (item) {
                        $scope.form.faults[item.ID] = false;
                    });

                    findReclamation($scope, order.ID);

                    var accessTokenName = $config.ACCESS_TOKEN_NAME;

                    var header = {};
                    header[accessTokenName] = AuthDataService.getAccessToken();

                    $scope.uploader = new FileUploader({
                        'headers': header,
                        'autoUpload ': true
                    });

                    $scope.uploader.onProgressAll = function (progress) {
                        $scope.uploadProgress = progress;
                    };

                    $scope.uploader.filters.push({
                        name: 'imageFilter',
                        fn: function (item, options) {
                            var itemName = item.name.split('.');
                            var lastItem = itemName.pop();
                            var possibleExtensions = ['jpg', 'jpeg','webp'];

                            if (possibleExtensions.indexOf(lastItem) > -1) {
                                return true;
                            }
                            Notification.warning($filter('translate')('required_ext') + possibleExtensions.join(','));
                            return false;
                        }
                    });

                    $scope.save = function () {

                        console.log(this.form);

                        if (this.form.products === undefined || this.form.products.length === 0) {
                            Notification.error($filter('translate')('select_at_least_one_product'));
                            return;
                        }

                        var sum = _.reduce(this.form.faults, function (memo, num) {
                            if (num === true) {
                                return ++memo;
                            }
                            return memo;
                        }, 0);

                        if (sum === 0) {
                            Notification.error($filter('translate')('select_fault_description'));
                            return;
                        }

                        ReclamationService.create(this.form, order.ID).then(function (data) {
                            if (data.response === true) {

                                if ($scope.uploader.queue.length > 0) {
                                    changeUrl($scope, data.item.ID).then(function () {
                                        $scope.uploader.uploadAll();
                                        $scope.uploader.onCompleteAll = function () {
                                            findReclamation($scope, order.ID);
                                            Notification.success($filter('translate')('reclamation_created'));
                                        }
                                    });
                                } else {
                                    findReclamation($scope, order.ID);
                                    Notification.success($filter('translate')('reclamation_created'));
                                }

                            }
                        });
                    };

                    $scope.savePrices = function () {

                        var prices = this.form.price;

                        DpOrderService.changeOrderPrice(order.ID, this.form).then(function (changePriceData) {
                            console.log(changePriceData);
                            if (changePriceData.saved === true) {
                                $scope.reclamation.pricesChanged = 1;
                                getProducts(order.ID).then(function (products) {
                                    $scope.products = products;
                                });
                            }

                            if (changePriceData.info) {
                                Notification.error($filter('translate')(changePriceData.info));
                            }
                        });

                    };

                    $scope.restoreOrderPrice = function (order) {
                        DpOrderService.restoreOrderPrice(order.ID).then(function (restoreData) {
                            if (restoreData.response === true) {
                                $scope.reclamation.pricesChanged = 0;
                                getProducts(order.ID).then(function (products) {
                                    $scope.products = products;
                                });
                            }
                        });
                    };

                    $scope.notEmptyPrices = function () {

                        var pricesEmpty = checkPriceValues(this, 'prices');
                        var pricePercentEmpty = checkPriceValues(this, 'pricesPercent');

                        if (pricesEmpty && pricePercentEmpty) {
                            $scope.showPercentPrices = true;
                            $scope.showNormalPrices = true;
                        }
                        if (!pricesEmpty && pricePercentEmpty) {
                            $scope.showPercentPrices = false;
                            $scope.showNormalPrices = true;
                        }
                        if (pricesEmpty && !pricePercentEmpty) {
                            $scope.showPercentPrices = true;
                            $scope.showNormalPrices = false;
                        }
                    };

                    $scope.formatSizeUnits = function (bytes) {
                        return MainWidgetService.formatSizeUnits(bytes);
                    };

                    $scope.removeFile = function (fileItem) {
                        fileItem.remove();
                    };

                    $scope.cancelUpload = function () {
                        $scope.uploader.clearQueue();
                    };

                    $scope.cancel = function () {
                        $modalInstance.close();
                    };
                }
            });

        };

        $scope.openExporter = function () {
            $modal.open({
                templateUrl: 'src/orders/templates/modalboxes/orderExporter.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.dateStart = "";
                    $scope.dateEnd = "";
                    $scope.exportOrder = function () {
                        //$modalInstance.close();
                        var timeFrame = {};
                        if ($scope.dateStart != "" && $scope.dateEnd != "") {
                            timeFrame.dateStart = $scope.dateStart;
                            timeFrame.dateEnd = $scope.dateEnd;
                        }
                        console.log(timeFrame);
                        DpProductService.exportOrders(timeFrame).then(function (data) {
                            console.log(data);
                            if (data.response) {
                                $modal.open({
                                    templateUrl: 'shared/templates/modalboxes/files.html',
                                    scope: $scope,
                                    size: 'sm',
                                    controller: function ($scope, $modalInstance) {
                                        $scope.filesTitle = 'orders_export';
                                        $scope.files = [data.url];
                                        $scope.fileLabel = 'filesLabel';
                                    }
                                });
                            } else {
                                Notification.error(Notification.error($filter('translate')('error')));
                            }
                        });
                    };

                }
            });
        };

        function changeUrl(scope, reclamationID) {

            var def = $q.defer();

            _.each(scope.uploader.queue, function (item, index) {
                item.url = ReclamationService.getUploadUrl(reclamationID);
                if (index === scope.uploader.queue.length - 1) {
                    def.resolve(true);
                }
            });

            return def.promise;
        }

        function findReclamation(scope, orderID) {
            ReclamationService.findByOrder(orderID).then(function (reclamation) {
                if (reclamation && reclamation.ID) {
                    scope.reclamationExist = true;
                    scope.reclamation = reclamation;
                    var idx;

                    if (typeof (reclamation.products) === 'string') {

                        scope.products = _.filter(scope.products, function (num) {
                            var reclamationProducts = reclamation.products.split(',').map(function (item) {
                                return parseInt(item, 10);
                            });
                            idx = _.indexOf(reclamationProducts, num.productID);
                            if (idx > -1) {
                                return true;
                            }
                        });

                    } else {

                        scope.products = _.filter(scope.products, function (num) {
                            var reclamationProduct = parseInt(reclamation.products, 10);
                            if (reclamationProduct === num.productID) {
                                return true;
                            }
                        });

                    }

                }
            }, function (error) {
                scope.reclamationExist = false;
            });
        }

        function checkPriceValues(context, key) {
            if (context.form[key] === undefined) {
                return true;
            }
            var anyEmpty = 0;
            _.each(context.form[key], function (value) {
                if (value.length > 0) {
                    anyEmpty++;
                }
            });

            return !(anyEmpty > 0);
        }

        function getProducts(orderID) {

            var def = $q.defer();

            DpProductService.getByOrder(orderID).then(function (products) {
                def.resolve(products);
            });

            return def.promise;
        }

        $scope.showCalcFiles = function (setID) {

            var files = CalcFileService.getAll(setID).then(function (data) {
                $modal.open({

                    templateUrl: 'src/orders/templates/modalboxes/calcFiles.html',
                    scope: $scope,
                    size: 'lg',
                    controller: function ($scope, $modalInstance) {

                        $scope.calcFiles = data;
                        console.log('$scope.calcFiles: ', $scope.calcFiles);

                    }
                });
            });
        };
        $scope.history = function (order, product) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/calculation-history.html',
                scope: $scope,
                size: 'lg',
                windowClass: 'modal-wide-screen',
                resolve: {
                    calculations: function (CalculationService) {
                        return CalculationService.history(product.baseID).then(function (data) {
                            return data;
                        }, function (data) {
                            console.error(data);
                            Notification.error($filter('translate')('data_retrieve_failed'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, calculations) {
                    $scope.calculations = calculations;
                    $scope.order = order;
                    $scope.edit = function (calculation) {
                        var data = _.extend(product, {calcID: calculation.ID});
                        $scope.$parent.edit(order, data);
                        $modalInstance.close();
                    }
                }
            });
        };
        $scope.edit = function (order, product) {
            var params = {
                'orderID': order.ID,
                'groupID': product.groupID,
                'typeID': product.typeID,
                'calcID': product.calcID,
                'productID': product.productID
            };
            $state.go('create-order-calc', params);
        };
        $scope.deliveriesHistory = function (order, product) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/delivery-history.html',
                scope: $scope,
                size: 'lg',
                windowClass: 'modal-wide-screen',
                resolve: {
                    deliveries: function (CalculationService) {
                        return CalculationService.deliveriesHistory(order.ID).then(function (data) {
                            return data;
                        }, function (data) {
                            console.error(data);
                            Notification.error($filter('translate')('data_retrieve_failed'));
                        });
                    }
                },
                controller: function ($scope, $modalInstance, deliveries) {
                    $scope.deliveries = deliveries;
                    $scope.order = order;
                    $scope.editDelivery = function (order, delivery) {
                        $scope.$parent.editDelivery(order, delivery);
                        $modalInstance.close();
                    }
                }
            });
        };
        $scope.editDelivery = function (order, delivery) {
            var params = {
                'orderID': order.ID,
                'edit': 1,
                'ver': delivery.ver
            };
            $state.go('order-make-order', params);
        };
    });
