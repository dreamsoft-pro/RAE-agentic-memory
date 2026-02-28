angular.module('dpClient.helpers')
    .directive('deliveries', function () {
        return {
            restrict: 'E',
            scope: {products: '=', baseProductAddresses: '=', deliveryConnected: '=', inCart: '=', title: '='},
            replace: true,
            templateUrl: 'views/deliveries.html',
            controller: function ($scope, $rootScope, Notification, DeliveryService, AddressService,
                                  DeliveryWidgetService, AddressWidgetService, DpCartsDataService, DpOrderService,
                                  $q, $filter, $timeout) {

                $scope.productAddresses = $scope.products[0].addresses ?? [{}];

                $scope.deliveryLackOfVolume = 0;
                /**
                 * Number of volume assigned to newly separated address
                 */
                $scope.separateVolume;

                $scope.filteredDeliveries

                $rootScope.$watch('logged', function (logged) {
                    if (logged != undefined) {
                        $scope.logged = logged;
                    }

                });

                $rootScope.$on('calculation', function (e, calculation) {
                    if ($scope.inCart) {
                        return;
                    }
                    $scope.calculation = _.clone(calculation, true);
                    updateCalculationWeight();
                    $scope.calculcateDeliveryPrice();

                });

                $rootScope.$on('addressesChanged', function () {
                    readData()
                });
                function getDeliveries() {
                    const def = $q.defer()
                    DeliveryService.getAll($rootScope.currentCurrency.code)
                        .then(function (data) {
                            def.resolve(data)
                        }, function (err) {
                            def.reject(err)
                        })
                    return def.promise;
                }


                function getAddresses() {
                    var def = $q.defer();

                    if ($rootScope.logged) {

                        AddressService.getForUser().then(function (data) {
                            def.resolve(data);
                        });

                    } else {
                        AddressService.getAddressesFromSession().then(function (addresses) {
                            AddressService.getAll(addresses).then(function (data) {
                                def.resolve(data);
                            });
                        });
                    }

                    return def.promise;
                }
                function readData(){
                    $q.all([getAddresses(), getDeliveries()]).then(data => {
                        $scope.addresses = data[0].addresses;
                        if($scope.addresses.length==1){
                            _.each($scope.productAddresses, (pa)=>{
                                pa.addressID = $scope.addresses[0].ID
                            })
                        }
                        $scope.senders = data[0].senders ?? null;
                        $scope.deliveries = data[1]
                        updateCalculationWeight()
                        $scope.calculcateDeliveryPrice();
                    })
                }
                readData();

                function setAddresses(allAddress) {
                    $scope.addresses = allAddress.addresses;
                    if (_.size(allAddress.senders) > 0) {
                        $scope.senders = [];
                        _.each(allAddress.senders, function (item) {
                            item.name = $filter('translate')(item.name);
                            $scope.senders.push(item);
                        });
                    }
                }

                $scope.addressesEdit = function () {
                    AddressWidgetService.addressesEdit($scope);
                };

                $scope.calculcateDeliveryPrice = function () {
                    $scope.filteredDeliveries = DeliveryWidgetService.filterDeliveries2($scope.deliveries, $scope.products)
                    var deliveryPrice = 0;
                    var deliveryGrossPrice = 0;
                    _.each($scope.productAddresses, function (address) {

                        var idx = _.findIndex($scope.filteredDeliveries, {ID: address.deliveryID});

                        if (idx > -1) {

                            if (typeof updateCalculationUrl != 'undefined') {
                                updateCalculationUrl('deliveryID', address.deliveryID);
                            }

                            if ($scope.filteredDeliveries[idx].module.func === 'collectionAttributes') {
                                address.turnOffAddress = true;
                                $scope.collectionPoints = address.collectionPoints = $scope.filteredDeliveries[idx].collectionPoints;
                                address.collectionPointID = $scope.filteredDeliveries[idx].collectionPoints[0].ID;
                            } else {
                                address.turnOffAddress = false;
                                address.collectionPoints = [];
                                delete address.collectionPointID;
                            }

                            if ($scope.filteredDeliveries[idx].hasParcelShops && address.parcelShops) {

                                address.hasParcelShops = true;

                            } else if ($scope.filteredDeliveries[idx].hasParcelShops && !address.parcelShops) {

                                address.hasParcelShops = true;
                                address.parcelShops = null;

                                DeliveryWidgetService.findParcelShops(
                                    address.addressID,
                                    $scope.filteredDeliveries[idx].ID,
                                    $scope.filteredDeliveries[idx].courierID,
                                    address
                                ).then(function (result) {
                                    console.log('findParcelShops ??? ' + result);
                                });

                            } else {
                                address.hasParcelShops = false;
                                address.parcelShops = null;
                            }

                            if (angular.isDefined($scope.filteredDeliveries[idx].price)) {

                                DeliveryWidgetService.checkExclusions($scope, address);

                                const packagingData = DeliveryWidgetService.getAddressPackaging(
                                    $scope.inCart ? $scope.products : [$scope.calculation],
                                    address.deliveryID,
                                    $scope.deliveryConnected ? undefined : address.allVolume,
                                    $scope.deliveries
                                )
                                address = _.copyProperties(packagingData, ['no_of_pkgs', 'grossweight', 'price', 'priceGross'], address)

                            } else {
                                address.price = 0;
                            }

                        } else {
                            address.price = 0;
                        }

                    });
                    $rootScope.$emit('delivery', _.clone($scope.productAddresses, true))
                };

                function updateCalculationWeight() {
                    if ($scope.productAddresses[0]) {
                        if (!$scope.productAddresses[0].deliveryID) {
                            if (!$scope.deliveries || !$scope.addresses) {
                                return
                            }
                            $scope.productAddresses[0].deliveryID = $scope.deliveries[0].ID;
                            if ($rootScope.logged) {
                                $scope.productAddresses[0].addressID = $scope.addresses.find(address => address.default).ID;
                            }
                            if ($scope.senders) {
                                $scope.productAddresses[0].senderID = $scope.senders[0].type;
                            }

                        }
                    } else {
                        console.warn('Brak productAddresses')
                    }

                    if (!$scope.inCart) {
                        $scope.productAddresses[0].weight = $scope.calculation.weight;
                        $scope.productAddresses[0].volume = $scope.calculation.volume;
                        $scope.productAddresses[0].amount = $scope.calculation.amount;
                        $scope.productAddresses[0].allVolume = $scope.calculation.volume * $scope.calculation.amount;
                    }
                }


                var _timeout;
                $scope.changeVolumes = function () {
                    $scope.calculcateDeliveryPrice()
                    var _this = this;
                    if (_timeout) {
                        $timeout.cancel(_timeout);
                    }

                    const allVolumes = _.reduce($scope.productAddresses, (all, item) => all + parseInt(item.allVolume), 0);

                    _timeout = $timeout(function () {

                        var selectedVolume = $scope.products[0].volume * $scope.products[0].amount;

                        if (allVolumes > selectedVolume) {
                            var over = allVolumes - selectedVolume;

                            $scope.productAddresses[_this.$index].allVolume -= Number(over);
                            $scope.deliveryLackOfVolume = 0;

                            Notification.error($filter('translate')('volume_exceeded_by') + ' ' + over);

                        } else if (allVolumes <= selectedVolume) {

                            $scope.deliveryLackOfVolume = Number(selectedVolume - allVolumes);

                        }

                        _timeout = null;
                    }, 500);
                };

                $scope.separateDelivery = function () {

                    const newVolume = parseInt($scope.separateVolume);

                    if (newVolume <= 0 || _.isNaN(newVolume)) {
                        Notification.error($filter('translate')('enter_volume'));
                        return;
                    }
                    if ($scope.deliveryLackOfVolume < 0) {
                        $scope.deliveryLackOfVolume = 0;
                    }


                    const availableVolumes = Number($scope.productAddresses[0].allVolume + $scope.deliveryLackOfVolume);

                    let diffVolume;

                    if (newVolume === availableVolumes) {
                        Notification.error($filter('translate')('enter_less_volume'));
                        return;
                    }
                    if (newVolume > availableVolumes) {
                        diffVolume = newVolume - availableVolumes;
                        Notification.error($filter('translate')('volume_exceeded_by') + ' ' + diffVolume);
                        return;
                    }

                    if (newVolume <= $scope.deliveryLackOfVolume) {
                        $scope.deliveryLackOfVolume = $scope.deliveryLackOfVolume - newVolume;
                    } else {

                        diffVolume = Number(newVolume - $scope.deliveryLackOfVolume);

                        if (diffVolume === $scope.productAddresses[0].allVolume) {
                            Notification.error($filter('translate')('enter_less_volume'));
                            return;
                        }

                        if (diffVolume > $scope.productAddresses[0].allVolume) {
                            var over = Number(diffVolume - $scope.productAddresses[0].allVolume);
                            Notification.error($filter('translate')('volume_exceeded_by') + ' ' + over);
                            return;
                        }

                        $scope.deliveryLackOfVolume = 0;
                        if (diffVolume > 0 && diffVolume < $scope.productAddresses[0].allVolume) {
                            $scope.productAddresses[0].volume = Number($scope.productAddresses[0].volume - diffVolume);
                            $scope.productAddresses[0].allVolume = Number($scope.productAddresses[0].allVolume - diffVolume);
                        }

                    }

                    const newIndex = _.findLast($scope.productAddresses).index + 1;
                    const lastIndex = $scope.productAddresses.push({
                        'volume': newVolume,
                        'allVolume': newVolume,
                        'index': newIndex
                    }) - 1;
                    $scope.productAddresses[lastIndex].deliveryID = $scope.productAddresses[0].deliveryID;
                    $scope.productAddresses[lastIndex].addressID = $scope.productAddresses[0].addressID;
                    $scope.productAddresses[lastIndex].senderID = $scope.productAddresses[0].senderID;
                    $scope.productAddresses[lastIndex].parcelShops = $scope.productAddresses[0].parcelShops;

                    $scope.changeVolumes($scope.productAddresses[lastIndex]);
                    $scope.calculcateDeliveryPrice();
                };

                $scope.saveAddresses = function (products) {
                    const def = $q.defer()
                    DeliveryWidgetService.reducePostData(products[0].addresses)
                        .then(function (productAddresses) {
                            products.forEach((product, productIdx) => {
                                AddressService.updateProductAddresses(product.orderID, product.productID, productAddresses)
                                    .then(function (savedData) {
                                        if (savedData.response === true) {
                                            const cartData = _.copyProperties(product, ['orderID', 'productID']);
                                            cartData.productAddresses = products[0].addresses;
                                            DpCartsDataService.update(cartData)
                                                .then(function (patchResponse) {
                                                    if (patchResponse.response === true) {
                                                        DpOrderService.changeAddresses(product.orderID, product.productID, productAddresses).then(function (updateData) {
                                                            if (updateData.response && productIdx == products.length - 1) {
                                                                Notification.success($filter('translate')('saved_message'));
                                                                def.resolve()
                                                            }
                                                        });
                                                    } else {
                                                        Notification.error($filter('translate')('error'));
                                                        def.reject()
                                                    }
                                                });
                                        } else {
                                            Notification.error($filter('translate')('error'));
                                            def.reject()
                                        }
                                    });
                            })


                        });
                    return def.promise;

                };

                $scope.removeProductAddress = function (idx) {
                    const oldVolume = Number($scope.productAddresses[idx].allVolume);
                    $scope.productAddresses.splice(idx, 1);
                    $scope.productAddresses[0].allVolume = Number($scope.productAddresses[0].allVolume) + oldVolume;
                    $scope.calculcateDeliveryPrice()
                };

                $scope.getFlagClass = (addresses, addressID) => `flag-icon-${addresses.find(address => address.ID == addressID).countryCode.toLowerCase()}`;

                $scope.senderNameFn = item => $filter('translate')(item.name)
                $scope.compareSender = (item, address) => item.type == address.senderID;
                $scope.senderSelect = (item, address) => {
                    address.senderID = item.type;
                    if ($scope.inCart) {
                        $scope.saveAddresses($scope.products)
                    }

                }

                $scope.deliveryNameFn = item => item.names[$rootScope.currentLang.code];
                $scope.compareDelivery = (item, address) => item.ID == address.deliveryID
                $scope.deliverySelect = (item, address) => {
                    if(!address.addressID){
                        Notification.info($filter('translate')('select_address') );
                        return
                    }
                    address.deliveryID = item.ID
                    if ($scope.inCart) {
                        $scope.saveAddresses($scope.products).then(() => {
                            $scope.calculcateDeliveryPrice();
                        })
                    } else {
                        $scope.calculcateDeliveryPrice();
                    }

                }

                $scope.addressNameFn = item => item.addressName;
                $scope.compareAddress = (item, address) => item.ID == address.addressID
                $scope.addressSelect = (item, address) => {
                    address.addressID = item.ID;
                    if ($scope.inCart) {
                        $scope.saveAddresses($scope.products)
                    }

                }
                $scope.getAddressType = (address) => {
                    if (address.collectionPointID) {
                        return 'collectionPoint'
                    } else {
                        return 'address'
                    }
                }
                $scope.compareColPoint = (item, address) => item.ID == address.collectionPointID
                $scope.collectionPointNameFn = (item) => item.langs[$rootScope.currentLang.code].name
                $scope.colPointSelect = (item, address) => {
                    address.collectionPointID = item.ID
                    if ($scope.inCart) {
                        $scope.saveAddresses($scope.products)
                    }
                }

            }
        };
    });
