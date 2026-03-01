/*global angular*/
'use strict';

angular.module('digitalprint.app')
    .controller('customerservice.OrderMakeOrderCtrl', function ($stateParams, order, $scope, DpOrderService,
                                                                UserAddressService, DeliveryService, UserService,
                                                                DpUserAddressService, ApiCollection, $state, $filter,
                                                                $modal, Notification, PaymentService) {

        $scope.order = {};
        $scope.deliveries = [];
        $scope.payments = [];

        if (!order.userID) {
            Notification.error('Brak usera');
        }
        if (!order.domainID) {
            Notification.error('No domainID for User');
        }

        $scope.edit = !!$stateParams.edit;

        var UserAddress = new UserAddressService(order.userID);
        UserAddress.getAllAddresses().then(function (data) {
            $scope.userAddresses = data;
        }, function (data) {
            Notification.error($filter('translate')('data_retrieve_failed'));
        });

        var UserAddressInvoice = new UserAddressService(order.userID);
        UserAddress.getAllAddressesVat().then(function (data) {
            $scope.hasInvoiceAddress = data.length > 0;
            $scope.userAddressesInvoice = data;
        }, function (data) {
            Notification.error($filter('translate')('data_retrieve_failed'));
        });

        DeliveryService.getAllForDomain(order.domainID).then(function (data) {
            $scope.deliveries = data;
        }, function (data) {
            Notification.error($filter('translate')('data_retrieve_failed'));
        });

        PaymentService.getAll().then(function (data) {
            $scope.payments = data;
        }, function (data) {
            Notification.error($filter('translate')('data_retrieve_failed'));
        });

        function init() {
            $scope.resetData();
        }

        $scope.addAddress = function () {
            if (!$scope.order.addresses) {
                $scope.order.addresses = [];
            }
            $scope.order.addresses.push({
                products: [{}]
            });
        };

        $scope.removeAddress = function (idx) {
            $scope.order.addresses.splice(idx, 1);
        };

        $scope.resetData = function () {

            $scope.hasInvoiceAddress = false;

            $scope.order = _.clone(order, true);
            if (!$scope.order.addresses) {
                $scope.addAddress();
            }


            _.each($scope.order.addresses, function (address) {
                address.addressID = address.copyFromID;

                if (!address.products) {
                    $scope.addProduct(address);
                }
            });

        };


        $scope.addProduct = function (orderAddress) {
            orderAddress.products = [];
            if (orderAddress.productID) {
                var product = _.clone(_.findWhere($scope.order.products, {productID: orderAddress.productID}), true);
                product.volume = orderAddress.volume;
                orderAddress.products.push(product);
            }
        };

        $scope.removeProduct = function (orderAddress, idx) {
            orderAddress.products.splice(idx, 1);
        };

        $scope.selectProduct = function (addressProduct) {
            if (addressProduct.productID === null) {
                addressProduct.volume = null;
            }
        };

        $scope.makeOrder = function () {

            var actInvoiceAddressID = null;

            if (!angular.isDefined($scope.order.invoiceAddress)) {
                actInvoiceAddressID = null;
            } else {
                actInvoiceAddressID = $scope.order.invoiceAddress.copyFromID;
            }

            var data = {
                invoiceAddressID: actInvoiceAddressID
            };

            if(angular.isDefined($scope.order.sendMailToUser) && parseInt($scope.order.sendMailToUser) === 1) {
                data.sendMailToUser = $scope.order.sendMailToUser;
            }

            data.paymentID = $scope.order.paymentID;

            data.changeReason = $scope.order.changeReason;

            data.addresses = {};
            var addressObject = {};
            var commonDelivery = false;

            var amount;

            if( $scope.order.addresses.length === 1 ) {
                var oneAddress = _.first($scope.order.addresses);

                if( _.first(oneAddress.products).productID === null ||
                    _.first(oneAddress.products).productID === undefined ) {
                    _.each($scope.order.products, function(oneProduct) {

                        addressObject = {};
                        addressObject.deliveryID = oneAddress.deliveryID;
                        addressObject.addressID = oneAddress.addressID;
                        addressObject.volume = oneProduct.volume * oneProduct.amount;
                        addressObject.amount = oneProduct.amount;
                        addressObject.senderID = 1;
                        if(!commonDelivery) {
                            addressObject.commonDeliveryID = commonDelivery = oneAddress.deliveryID;
                        } else {
                            addressObject.commonDeliveryID = commonDelivery;
                        }
                        addressObject.join = true;
                        data.addresses[oneProduct.ID] = [];
                        data.addresses[oneProduct.ID].push(addressObject);
                    });
                } else {

                    if( $scope.order.products.length > 1 ) {
                       Notification.warning($filter('translate')('add_more_address_or_join_delivery'));
                       return;
                    }
                }
            } else {

                _.each($scope.order.addresses, function( oneAddress ) {

                    var idx = _.findIndex(order.products, {produtID: _.first(oneAddress.products).productID});
                    amount = 1;
                    if( idx > -1 ) {
                        amount = order.products[idx].amount;
                    }

                    addressObject = {};
                    addressObject.deliveryID = oneAddress.deliveryID;
                    addressObject.addressID = oneAddress.addressID;
                    addressObject.baseID = oneAddress.ID;
                    addressObject.volume = parseInt(_.first(oneAddress.products).volume);
                    addressObject.senderID = 1;
                    addressObject.amount = amount;
                    var oneProduct=_.first(oneAddress.products);
                    var calcID=oneProduct.calcID?oneProduct.calcID:oneProduct.productID;
                    if( data.addresses[calcID] === undefined ) {
                        data.addresses[calcID] = [];
                    }
                    data.addresses[calcID].push(addressObject);
                });

            }

            if( !_.isEmpty(data.addresses) ) {

                var verificationSummary = {};

                _.each(data.addresses, function( verificationDeliveries, keyCalcID ) {

                    _.each(verificationDeliveries, function(verificationDelivery) {

                        if( verificationSummary[keyCalcID] === undefined ) {
                            verificationSummary[keyCalcID] = parseInt(verificationDelivery.volume);
                        } else {
                            verificationSummary[keyCalcID] += parseInt(verificationDelivery.volume);
                        }

                    });
                });

                var validationError = false;
                var rightAmount;

                _.each(verificationSummary, function( volume, keyCalcID ) {

                    var foundProduct = _.findWhere($scope.order.products, {calcID: parseInt(keyCalcID)});

                    rightAmount = foundProduct.volume * foundProduct.amount;

                    if( rightAmount !== parseInt(volume) ) {
                        validationError = $filter('translate')('wrong_amount') + ', product: ' + foundProduct.ID;
                    }
                });


                if( validationError.length > 0 ) {
                    Notification.error( validationError );
                    return;
                }

            } else {
                Notification.error($filter('translate')('error'));
                return;
            }

            DpOrderService.makeOrder(order.ID, data).then(function (data) {
                Notification.success($filter('translate')('success'));
                $state.go('orders-orders');
            }, function (data) {
                Notification.error($filter('translate')('error'));
                if (data.warning) {
                    $scope.alert = true;
                    _.each(data.warning, function (value, key) {
                        $scope.alertValueExceeded = Math.abs(value);
                        if (value < 0) {
                            $scope.alertExceededText = $filter('translate')('volume_exceeded_by');
                        } else {
                            $scope.alertExceededText = $filter('translate')('volume_too_low');
                        }

                    });
                }
            });
        };

        $scope.addresses = function (userID) {

            var user = UserService.getUser(userID);

            var AddressBook = new DpUserAddressService(userID);

            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/addresses.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    addresses: function (DpUserAddressService) {
                        return AddressBook.getAllAddresses().then(function (data) {
                            return data;
                        });
                    },
                    addressesVat: function (DpUserAddressService) {
                        return AddressBook.getAllAddressesVat().then(function (data) {
                            return data;
                        });
                    },
                    userCanEdit: function (UserService) {
                        return UserService.canEditOtherAddress().then(function (data) {
                            return data.response;
                        }, function (data) {
                            return data.response;
                        });
                    },
                    userCanRemove: function (UserService) {
                        return UserService.canRemoveOtherAddress().then(function (data) {
                            return data.response;
                        }, function (data) {
                            return data.response;
                        });
                    },
                    canAddOtherAddress: function (UserService) {
                        return UserService.canAddOtherAddress().then(function (data) {
                            return data.response;
                        }, function (data) {
                            return data.response;
                        });
                    },
                    countries: function(CountriesService) {
                        return CountriesService.getAllEnabled().then( function(dataCountries) {
                            return dataCountries;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, addresses, addressesVat, userCanEdit, userCanRemove,
                                      canAddOtherAddress, countries) {

                    $scope.user = user;
                    $scope.addresses = addresses;
                    $scope.addressesVat = addressesVat;
                    $scope.userCanEdit = userCanEdit;
                    $scope.userCanRemove = userCanRemove;
                    $scope.canAddOtherAddress = canAddOtherAddress;
                    $scope.countries = countries;

                    $scope.addAddress = function () {
                        $scope.form.type = 1;

                        AddressBook.createAddress($scope.form).then(function (data) {

                            if ($scope.form.default == 1) {
                                angular.forEach($scope.addresses, function (value, key) {
                                    $scope.addresses[key].default = 0;
                                });
                            }

                            $scope.addresses.push(data.item);
                            $scope.userAddresses.push(data.item);
                            $scope.form = {};

                            Notification.success($filter('translate')('success'));

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.addAddressVat = function () {

                        $scope.form.add.type = 2;

                        AddressBook.createAddress($scope.form.add).then(function (data) {

                            if ($scope.form.add.default == 1) {
                                angular.forEach($scope.addressesVat, function (value, key) {
                                    $scope.addressesVat[key].default = 0;
                                });
                            }

                            $scope.userAddressesInvoice.push(data.item);
                            $scope.addressesVat.push(data.item);
                            $scope.form.add = {};


                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.editAddress = function (item) {

                        var tmp = _.clone(item, true);
                        item.edit = _.clone(item, true);

                        $scope.save = function () {

                            AddressBook.edit(item.edit).then(function (data) {

                                if (item.edit.default == 1) {
                                    angular.forEach($scope.addresses, function (value, key) {
                                        if ($scope.addresses[key].ID != item.edit.ID) {
                                            $scope.addresses[key].default = 0;
                                        }
                                    });
                                }

                                item = _.extend(item, item.edit);

                                angular.forEach($scope.userAddresses, function (value, key) {
                                    if (value.ID == item.ID) {
                                        $scope.userAddresses[key] = item;
                                    }
                                });

                                delete item.edit;
                                item.isCollapsed = false;

                                Notification.success($filter('translate')('success'));
                            }, function (data) {
                                item = _.extend(item, tmp);
                                Notification.error($filter('translate')('error'));
                            });
                        };

                        $scope.reset = function () {
                            item.edit = _.clone(item, true);
                        };
                    };

                    $scope.editAddressVat = function (item) {

                        var tmp = _.clone(item, true);
                        item.edit = _.clone(item, true);

                        $scope.save = function () {

                            AddressBook.edit(item.edit).then(function (data) {

                                if (item.edit.default == 1) {
                                    angular.forEach($scope.addressesVat, function (value, key) {
                                        if ($scope.addressesVat[key].ID != item.edit.ID) {
                                            $scope.addressesVat[key].default = 0;
                                        }
                                    });
                                }

                                //console.log(item.edit);
                                item = _.extend(item, item.edit);

                                angular.forEach($scope.userAddressesInvoice, function (value, key) {
                                    if (value.ID == item.ID) {
                                        $scope.userAddressesInvoice[key] = item;
                                    }
                                });

                                delete item.edit;
                                item.isCollapsed = false;

                                Notification.success($filter('translate')('success'));
                            }, function (data) {
                                item = _.extend(item, tmp);
                                Notification.error($filter('translate')('error'));
                            });
                        };

                        $scope.reset = function () {

                            item.edit = _.clone(item, true);

                        };

                    };

                    $scope.removeAddress = function (item) {

                        AddressBook.remove(item).then(function (data) {

                            var idx = _.findIndex($scope.addresses, {
                                ID: item.ID
                            });
                            var idxUsr = _.findIndex($scope.userAddresses, {
                                ID: item.ID
                            });
                            $scope.addresses.splice(idx, 1);
                            $scope.userAddresses.splice(idxUsr, 1);

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.removeAddressVat = function (item) {

                        AddressBook.remove(item).then(function (data) {

                            var idx = _.findIndex($scope.addressesVat, {
                                ID: item.ID
                            });
                            var idxUsr = _.findIndex($scope.userAddressesInvoice, {
                                ID: item.ID
                            });
                            $scope.addressesVat.splice(idx, 1);
                            $scope.userAddressesInvoice.splice(idxUsr, 1);

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                }
            });
        };

        init();
    });
