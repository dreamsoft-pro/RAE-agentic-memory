angular.module('digitalprint.app')
    .controller('customerservice.UsersListCtrl', function ($scope, $rootScope, $modal, $q, $filter, ApiCollection,
                                                           DpUserAddressService, UserService, Notification, $timeout,
                                                           DiscountService, CountriesService, CurrencyService, $state) {
        /**
         *
         * @type {number}
         */
        $scope.showRows = 25;
        $scope.usersConfig = {
            count: 'users/count',
            params: {
                limit: $scope.showRows
            },
            onSuccess: function (data) {
                $scope.usersCtrl.items = data;
            }
        };

        if ($state.params.userID) {
            $scope.usersConfig.params.ID = $state.params.userID;
        }

        $scope.sellers = [];
        $scope.countries = [];
        $scope.defaultCurrency = {};
        $scope.discountGroups = [];

        $scope.usersCtrl = new ApiCollection('users', $scope.usersConfig);
        $scope.usersCtrl.get();

        var updateTableTimeout;

        $scope.setParams = function () {
            $timeout.cancel(updateTableTimeout);
            updateTableTimeout = $timeout(function () {
                $scope.usersCtrl.get();
            }, 1000);
        };

        function init() {

            UserService.getUsersByType().then(function (data) {
                $scope.sellers = data;
            });

            CountriesService.getAllEnabled().then( function(dataCountries) {
                $scope.countries = dataCountries;
            });

            CurrencyService.getDefault().then( function(data) {
                $scope.defaultCurrency = data;
            });

            getDiscountGroups().then( function( discountGroups ) {
                $scope.discountGroups = discountGroups;
            });

        }

        init();

        function getDiscountGroups() {
            var def = $q.defer();

            DiscountService.getGroups().then(function (data) {
                def.resolve(data);
            });

            return def.promise;
        }

        function getSelectedDiscountGroups(userID) {
            var def = $q.defer();

            DiscountService.getSelectedGroups(userID).then(function (data) {
                def.resolve(data);
            });

            return def.promise;
        }

        $scope.addresses = function (user) {

            var userID = user.ID;
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
                    }
                },
                controller: function ($scope, $modalInstance, addresses, addressesVat, userCanEdit, userCanRemove, canAddOtherAddress) {

                    $scope.user = user;
                    $scope.addresses = addresses;
                    $scope.addressesVat = addressesVat;
                    $scope.userCanEdit = userCanEdit;
                    $scope.userCanRemove = userCanRemove;
                    $scope.canAddOtherAddress = canAddOtherAddress;

                    $scope.addAddress = function () {
                        $scope.form.type = 1;

                        AddressBook.createAddress($scope.form).then(function (data) {

                            if ($scope.form.default == 1) {
                                angular.forEach($scope.addresses, function (value, key) {
                                    $scope.addresses[key].default = 0;
                                });
                            }

                            $scope.addresses.push(data.item);
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

                                if( data.response ) {
                                    if (item.edit.default === 1) {
                                        angular.forEach($scope.addresses, function (value, key) {
                                            if ($scope.addresses[key].ID !== item.edit.ID) {
                                                $scope.addresses[key].default = 0;
                                            }
                                        });

                                        user.address = data.item;
                                    }

                                    item = _.extend(item, item.edit);
                                    delete item.edit;
                                    item.isCollapsed = false;

                                    Notification.success($filter('translate')('success'));

                                }

                            }, function (data) {
                                item = _.extend(item, tmp);
                                Notification.error($filter('translate')('error'));
                            });
                        };

                        $scope.reset = function () {
                            item.edit = _.clone(item, true);
                        }
                    };

                    $scope.editAddressVat = function (item) {

                        var tmp = _.clone(item, true);
                        item.edit = _.clone(item, true);

                        $scope.save = function () {

                            AddressBook.edit(item.edit).then(function (data) {

                                if( data.response ) {
                                    if (item.edit.default === 1) {
                                        angular.forEach($scope.addressesVat, function (value, key) {
                                            if ($scope.addressesVat[key].ID !== item.edit.ID) {
                                                $scope.addressesVat[key].default = 0;
                                            }
                                        });

                                        user.fvAddress = data.item;
                                    }

                                    item = _.extend(item, item.edit);
                                    delete item.edit;
                                    item.isCollapsed = false;

                                    Notification.success($filter('translate')('success'));
                                }

                            }, function (data) {
                                item = _.extend(item, tmp);
                                Notification.error($filter('translate')('error'));
                            });
                        };

                        $scope.reset = function () {

                            item.edit = _.clone(item, true);

                        }

                    };

                    $scope.removeAddress = function (item) {

                        AddressBook.remove(item).then(function (data) {

                            var idx = _.findIndex($scope.addresses, {
                                ID: item.ID
                            });
                            $scope.addresses.splice(idx, 1);

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
                            $scope.addressesVat.splice(idx, 1);

                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }

                }
            });
        };

        $scope.loadusers = function () {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/customers-order.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {

                }
            });
        };

        $scope.editUserData = function (user) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/edit-user-data.html',
                scope: $scope,
                size: 'lg',
                resolve: {
                    userCanEdit: function (UserService) {
                        return UserService.canEditOtherAddress().then(function (data) {
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
                    currencies: function(CurrencyService) {
                        return CurrencyService.getAll().then(function(data) {
                            return _.filter(data, function(one) {
                                return !!one.active;
                            })
                        }, function() {
                            return [];
                        });
                    },
                    languages: function(LangSettingsService) {
                        return LangSettingsService.getAll().then( function(data) {
                            return data;
                        })
                    }
                },
                controller: function ($scope, $modalInstance, userCanEdit, canAddOtherAddress, currencies, languages) {
                    $scope.currencies = currencies;
                    $scope.user = user;

                    $scope.userCanEdit = userCanEdit;
                    $scope.canAddOtherAddress = canAddOtherAddress;
                    $scope.languages = languages;

                    $scope.saveUserData = function() {

                        var that = this;
                        var userData = {
                            ID: this.user.ID,
                            user: this.user.user,
                            login: this.user.login,
                            name: this.user.name,
                            lastname: this.user.lastname
                        };

                        UserService.editUser(userData).then( function(savedInfo) {
                            if( savedInfo.response ) {
                                Notification.success($filter('translate')('saved_message'));
                                user = that.user;
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        }, function (error) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                    $scope.changePassword = function() {

                        var passwordData = {
                            ID: user.ID,
                            password: this.form.password,
                            passwordRepeat: this.form.passwordRepeat
                        };

                        if( this.form.password !== this.form.passwordRepeat ) {
                            Notification.error($filter('translate')('passwords_not_same'));
                            return;
                        }

                        UserService.changePassword(passwordData).then(function(savedInfo) {
                            if( savedInfo.response ) {
                                Notification.success($filter('translate')('password_changed'))
                            } else {
                                Notification.error($filter('translate')(savedInfo.info));
                            }
                        }, function (error) {
                            if( error.info ) {
                                Notification.error($filter('translate')(error.info));
                            } else {
                                Notification.error($filter('translate')('error'));
                            }
                        });
                    };

                    $scope.editDefaultAddress = function( addressType ) {

                        var addressKey = 'address';
                        var type = 1;
                        if( addressType === 'invoice' ) {
                            addressKey = 'fvAddress';
                            type = 2;
                        }

                        var AddressBook = new DpUserAddressService(this.user.ID);

                        var addressData = {
                            type: type,
                            userID: this.user.ID,
                            default: 1,
                            name: this.user[addressKey].name,
                            lastname: this.user[addressKey].lastname,
                            companyName: this.user[addressKey].companyName,
                            street: this.user[addressKey].street,
                            house: this.user[addressKey].house,
                            apartment: this.user[addressKey].apartment,
                            zipcode: this.user[addressKey].zipcode,
                            city: this.user[addressKey].city,
                            areaCode: this.user[addressKey].areaCode,
                            telephone: this.user[addressKey].telephone,
                            nip: this.user[addressKey].nip,
                            addressName: this.user[addressKey].addressName,
                            countryCode: this.user[addressKey].countryCode
                        };

                        if( !this.user[addressKey].ID ) {

                            AddressBook.createAddress(addressData).then(function (createData) {

                                if( createData.response ) {
                                    user[addressKey] = createData.item;
                                    Notification.success($filter('translate')('success'));
                                } else {
                                    Notification.error($filter('translate')('error'));
                                }

                            }, function (data) {
                                Notification.error($filter('translate')('error'));
                            });

                        } else {

                            addressData.ID = this.user[addressKey].ID;

                            AddressBook.edit(addressData).then(function (editedData) {

                                if( editedData.response ) {
                                    user[addressKey] = editedData.item;
                                    Notification.success($filter('translate')('success'));
                                } else {
                                    Notification.error($filter('translate')('error'));
                                }

                            }, function (data) {
                                Notification.error($filter('translate')('error'));
                            });

                        }

                    };

                    $scope.editAdditionalUserOptions = function(user) {

                        var data = {
                            'creditLimit': this.user.options.creditLimit,
                            currency: this.user.options.currency,
                            sellerID: this.user.userSellerID,
                            lang: this.user.options.lang
                        };

                        var saveResultCount = 0;

                        UserService.editUserOptions(user, data).then(function (data) {
                            if (data.response) {
                                saveResultCount++;
                                saveCallback(saveResultCount);
                            }
                        }, function (errorData) {

                        });

                        var userData = {
                            ID: user.ID,
                            domainID: this.user.domainID,
                            deferredPayment: this.user.deferredPayment,
                            block: this.user.block ? 1 : 0
                        };

                        UserService.editUser(userData).then( function(savedInfo) {
                            if( savedInfo.response ) {
                                saveResultCount++;
                                saveCallback(saveResultCount);
                            }
                        }, function (errorData) {

                        });

                    };

                    $scope.openAddressModal = function(user) {
                        $modalInstance.close();
                        $scope.$parent.addresses(user);
                    }
                }
            });
        };

        function saveCallback(saveResultCount) {
            if( saveResultCount > 1 ) {
                Notification.success($filter('translate')('saved_message'));
            }
        }

        $scope.changeDiscountGroup = function (user) {

            var data = {'discountGroupID': user.discountGroupID};
            UserService.editUserOptions(user, data).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });

        };

        $scope.changeUserSellerID = function (user) {

            var data = {'sellerID': user.userSellerID};
            UserService.editUserOptions(user, data).then(function (data) {
                if (data.response) {
                    Notification.success($filter('translate')('success'));
                }
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

        $scope.selectDiscountGroups = function (user) {

            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/select-discount-group.html',
                scope: $scope,
                resolve: {
                    discountGroups: function () {
                        return getSelectedDiscountGroups(user.ID).then(function (discountGroups) {
                            return discountGroups;
                        });
                    }
                },
                controller: function ($scope, $modalInstance, discountGroups) {

                    $scope.discountGroups = discountGroups;

                    $scope.form = {};

                    $scope.cancel = function () {
                        $modalInstance.dismiss('cancel');
                    };

                    $scope.form.discountGroups = [];

                    $scope.save = function () {

                        _.each($scope.discountGroups, function (discountGroup) {
                            if (discountGroup.selected === 1 || discountGroup.selected === true) {
                                var idx = _.findIndex($scope.form.discountGroups, discountGroup.ID);
                                if (idx === -1) {
                                    $scope.form.discountGroups.push(discountGroup.ID);
                                }

                            }
                        });

                        user.countDiscountGroups = $scope.form.discountGroups.length;

                        DiscountService.setSelectedGroups(user.ID, $scope.form.discountGroups).then(function (data) {

                            if (data.response === true) {
                                user.userDiscountGroups = data.userDiscountGroups;
                                Notification.success($filter('translate')('success'));
                                $modalInstance.dismiss('cancel');
                            } else {
                                Notification.error($filter('translate')('error'));
                            }

                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    };

                }
            });

        };

        $scope.removeFilters = function() {
            $scope.usersCtrl.params = {};
            $scope.usersCtrl.params.limit = $scope.showRows;
            $scope.usersCtrl.params.offset = 0;
        }

    });
