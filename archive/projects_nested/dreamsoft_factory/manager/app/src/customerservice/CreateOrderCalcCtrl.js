/* global angular, _, console */
    angular.module('digitalprint.app')
        .controller('customerservice.CreateOrderCalcCtrl', function ($state, $stateParams, getData, $timeout, $scope, $rootScope,
                                                                     $filter, $modal, $q, PsGroupService, PsTypeService,
                                                                     PsComplexService, PsAttributeService, PsFormatService,
                                                                     PsCalculateService, PsPageService, ApiCollection,
                                                                     Notification, UserService, OrderDataService,
                                                                     CustomProductService, typeOfResource, HelpersService, TaxService) {

            "use strict";
            var userID = $stateParams.userID;
            var orderID = $stateParams.orderID;
            var currentProductID = $state.params.productID;
            $scope.currentProductID = currentProductID;
            $scope.currentMultiOfferVolumes = [];

            var customProductID = $state.params.customProductID;

            var pageTimeout = null;
            var stopSelectCustomFormat = null;

            $scope.priceUpdated = false;

            $scope.typeOfResource = typeOfResource;

            $scope.group = $scope.currentGroup = getData.group;
            $scope.type = $scope.currentType = getData.type;
            $scope.currentUser = getData.user;
            $scope.currentCalc = getData.calc;
            $scope.currentProduct = getData.product;

            $scope.currentFormat = false;
            $scope.currentPages = false;
            $scope.productItem = {};

            $scope.volumes = {};
            $scope.calculation = {};
            $scope.calculationInfo = [];
            $scope.relatedFormats = [];
            $scope.complexGroups = [];
            $scope.complexID = 0;

            $scope.sellerForm = {};
            $scope.searchUser = '';
            $scope.orderOwner = false;
            $scope.customProduct = false;
            $scope.printTypes = {};
            $scope.formatTimePeriod = HelpersService.formatTimePeriod;

            if (currentProductID) {
                var CalculateService = new PsCalculateService(0, 0);
                CalculateService.getCurrentMultiOfferVolumes({ 'productID': currentProductID }).then(function (data) {
                    $scope.currentMultiOfferVolumes = data.currentMultiOfferVolumes;
                });
            }

            if ($scope.currentCalc) {
                $scope.productItem.volume = $scope.currentCalc.volume;
                $scope.productItem.amount = $scope.currentCalc.amount;

                $scope.sellerForm.oldPrice = $scope.currentCalc.price;
                $scope.sellerForm.searchUser = {
                    ID: $scope.currentCalc.uID,
                    user: $scope.currentCalc.userMail,
                    companyName: $scope.currentCalc.userCompanyName,
                    name: $scope.currentCalc.userName,
                    lastname: $scope.currentCalc.userLastname
                };
            } else {
                if ($scope.productItem.amount === undefined) {
                    $scope.productItem.amount = 1;
                }
            }

            $scope.specialAttributeTypes = [
                { 'type': 1, 'name': 'piece_symbol' },
                { 'type': 2, 'name': 'square_meters_symbol' },
                { 'type': 3, 'name': 'order' }
            ];

            if ($scope.currentProduct) {
                $scope.productItem.name = $scope.currentProduct.name;
            }

            if ($scope.currentUser) {
                $scope.sellerForm.searchUser = {
                    ID: $scope.currentUser.ID,
                    user: $scope.currentUser.user,
                    companyName: $scope.currentUser.companyName,
                    name: $scope.currentUser.name,
                    lastname: $scope.currentUser.lastname
                };
            }

            var AttributeService;
            var FormatService;
            var ComplexService;
            var PagesService;
            var CalculateService;

            OrderDataService.init();

            function init() {
                selectType($scope.type);

                if (customProductID) {
                    CustomProductService.getOne(customProductID).then(function (customProductData) {
                        $scope.customProduct = customProductData;
                    });
                }

                if (userID) {
                    UserService.getUser(userID).then(function (userInfo) {
                        $scope.orderOwner = userInfo;
                    });
                } else {
                    UserService.getLoggedUserData().then(function (userInfo) {
                        $scope.orderOwner = userInfo;
                    });
                }
                TaxService.getForProduct($scope.currentGroup.ID, $scope.currentType.ID).then(function (data) {
                    $scope.taxes = data;
                    var defaultTax = _.findWhere(data, { default: 1 });
                    if (defaultTax) {
                        $scope.productItem.taxID = defaultTax.ID;
                    } else {
                        console.error('Group ' + $scope.currentGroup.name + ' have not default tax');
                    }
                });
            }

            var selectType = function (type) {
                $scope.currentType = type;
                $scope.complexGroups = [];
                var promises = [];
                if (!!type.complex) {
                    $scope.complexID = type.ID;
                    ComplexService = new PsComplexService($scope.currentGroup.ID, type.ID);
                    ComplexService.getAll().then(function (data) {
                        _.each(data, function (item) {
                            promises.push($scope.getComplexGroup(item));
                        });
                    }, function (data) {
                        $scope.currentType = false;
                        Notification.error($filter('translate')('data_retrieve_failed'));
                    });
                } else {
                    var group = {
                        ID: null,
                        name: type.name,
                        productID: type.ID,
                        type: "other",
                        products: []
                    };

                    var product = {
                        groupID: type.groupID,
                        typeID: type.ID,
                        typeName: type.name
                    };
                    group.products.push(product);
                    promises.push($scope.getComplexGroup(group));
                }

                $q.all(promises).then(function (data) {
                    getPossibleTechnologies();
                    console.log('100% loaded!');
                }, function (data) {
                    console.error('Error in loading...', data);
                });
            };

            function getPossibleTechnologies() {
                CalculateService = new PsCalculateService(0, 0);
                prepareSelectedProducts().then(function (selectedProducts) {
                    CalculateService.possibleTechnologies({ 'products': selectedProducts }).then(function (data) {
                        $scope.printTypes = data;
                        if ($scope.currentCalc) {
                            _.each($scope.currentCalc.calcProducts, function (product) {
                                var printTypeIdx = _.findIndex(data[product.typeID], { printTypeID: product.printTypeID });
                                searchComplexGroup(product.typeID).then(function (complexGroup) {
                                    if (printTypeIdx > -1) {
                                        complexGroup.selectedProduct.data.printType = data[product.typeID][printTypeIdx];
                                        complexGroup.selectedProduct.data.printType.currentIndex = printTypeIdx;

                                        var workspaceIdx = _.findIndex(data[product.typeID][printTypeIdx].workspaces,
                                            { workspaceID: product.workspaceID });

                                        if (workspaceIdx > -1) {
                                            complexGroup.selectedProduct.data.workspace = data[product.typeID][printTypeIdx].workspaces[workspaceIdx];
                                        }
                                    }
                                });
                            });
                        }
                    });
                });
            }

            function prepareSelectedProducts() {
                var def = $q.defer();
                var selectedProducts = [];
                _.each($scope.complexGroups, function (complexGroup, index) {
                    selectedProducts.push({
                        typeID: complexGroup.selectedProduct.typeID,
                        formatID: complexGroup.selectedProduct.data.currentFormat.ID
                    });

                    if ($scope.complexGroups.length === index + 1) {
                        def.resolve(selectedProducts);
                    }
                });
                return def.promise;
            }

            $scope.getComplexGroup = function (group) {
                var def = $q.defer();
                $scope.complexGroups.push(group);
                _.each(group.products, function (item) {
                    if (!group.selectedProduct) {
                        if ($scope.currentCalc) {
                            var idx = _.findIndex($scope.currentCalc.calcProducts, { typeID: item.typeID });
                            if (idx === -1) {
                                return true;
                            }
                        }
                        $scope.selectComplexProduct(group, item).then(function (data) {
                            def.resolve(data);
                        }, function (data) {
                            def.reject(data);
                        });
                    }
                });
                return def.promise;
            };

            $scope.selectComplexProduct = function (complexGroup, selectedProduct) {
                var def = $q.defer();
                complexGroup.selectedProduct = selectedProduct;
                $scope.getProduct(selectedProduct).then(function (data) {
                    def.resolve(data);
                }, function (data) {
                    def.reject(data);
                });
                return def.promise;
            };

            function getCurrentCalcProduct(product) {
                var currentCalcProduct = null;
                if ($scope.currentCalc) {
                    currentCalcProduct = _.findWhere($scope.currentCalc.calcProducts, { typeID: product.typeID });
                }
                return currentCalcProduct;
            }

            $scope.getProduct = function (product) {
                var def = $q.defer();
                var newProductData = {
                    info: product,
                    selectedOptions: {},
                    attributeMap: [],
                    optionMap: [],
                    attrPages: {},
                    attributes: {},
                    currentFormat: false,
                    currentPages: product.currentPages,
                    excludedOptions: [],
                    formatExcluded: [],
                    thickness: {
                        values: {},
                        min: null,
                        max: null,
                        current: null
                    }
                };

                product.data = newProductData;
                var currentCalcProduct = getCurrentCalcProduct(product);

                AttributeService = new PsAttributeService(product.groupID, product.typeID);
                FormatService = new PsFormatService(product.groupID, product.typeID);
                PagesService = new PsPageService(product.groupID, product.typeID);

                $q.all([
                    FormatService.getPublic($scope.complexID),
                    PagesService.getAll(),
                    AttributeService.getFullOptions()
                ]).then(function (data) {
                    newProductData.formats = data[0];
                    newProductData.relatedFormats = _.clone(newProductData.formats, true);

                    newProductData.pages = data[1];
                    newProductData.attributes = data[2];

                    _.each(newProductData.attributes, function (attr) {
                        newProductData.attributeMap.push(attr.attrID);
                        newProductData.optionMap[attr.attrID] = [];
                        _.each(attr.options, function (opt) {
                            newProductData.optionMap[attr.attrID].push(opt.ID);
                        });
                    });

                    var formatIdx = 0;
                    if (currentCalcProduct) {
                        formatIdx = _.findIndex(newProductData.relatedFormats, { ID: currentCalcProduct.formatID });
                        if (formatIdx === -1) {
                            console.error('Nie znaleziono formatu takiego jak w wybranej kalkulacji');
                            return true;
                        }
                    }
                    $scope.selectFormat(newProductData, newProductData.relatedFormats[formatIdx]);

                    if (currentCalcProduct) {
                        $scope.selectPages(newProductData, currentCalcProduct.pages);
                    } else {
                        if (newProductData.pages.length && newProductData.pages[0].pages) {
                            $scope.selectPages(newProductData, newProductData.pages[0].pages);
                        }
                        if (newProductData.pages.length && newProductData.pages[0].minPages) {
                            $scope.selectPages(newProductData, newProductData.pages[0].minPages);
                        }
                    }

                    if (currentCalcProduct && currentCalcProduct.usePerSheet) {
                        newProductData.useForSheet = currentCalcProduct.usePerSheet;
                    }

                    def.resolve(data);
                }, function (data) {
                    def.reject(data);
                    $scope.goToProducts();
                    Notification.error($filter('translate')('data_retrieve_failed'));
                });
                return def.promise;
            };

            $scope.selectFormat = function (product, format) {
                product.currentFormat = format;
                if (!!format.custom) {
                    product.currentFormat.customWidth = format.minWidth - format.slope * 2;
                    product.currentFormat.customHeight = format.minHeight - format.slope * 2;
                }

                $scope.checkRelatedFormats(product, format);
                $scope.filterRelatedFormats();

                $scope.selectDefaultFormats().then(function (data) {
                    $scope.checkFormatExclusions(product);
                    setExclusionsAsync(product).then(function (exclusionEnd) {
                        if (exclusionEnd) {
                            $scope.selectDefaultOptions(product);
                        }
                    });
                }, function (data) {
                    console.log(data);
                });
            };

            function setExclusionsAsync(product) {
                var def = $q.defer();
                product.excludedOptions = _.clone(product.formatExcluded);
                _.each(product.attributes, function (attribute) {
                    attribute.filteredOptions = _.clone(attribute.options, true);
                });

                var optID = {};
                var activeAttrID;

                _.each(product.attributeMap, function (attrID) {
                    activeAttrID = attrID;
                    optID = product.selectedOptions[attrID];

                    if (optID) {
                        var item = {};

                        if (_.isObject(optID)) {
                            item = optID;
                        } else {
                            item = getOption(product, optID);
                        }

                        var tmpExclusions = {};
                        var exclusionsThickness = $scope.filterByThickness(product);
                        var exclusionsThicknessPages = $scope.filterByOptionsPages(product);

                        if (item.exclusions) {
                            tmpExclusions = _.merge({}, item.exclusions, exclusionsThickness, exclusionsThicknessPages);
                        }

                        if (tmpExclusions) {
                            setOptionExclusionsAsync(product, activeAttrID, tmpExclusions).then(function (deletedAttrs) {
                                checkAttrSelectAsync(product, deletedAttrs).then(function (isAttrSelectEnd) {
                                    if (isAttrSelectEnd) {
                                        if (_.last(product.attributeMap) === activeAttrID) {
                                            def.resolve(true);
                                        }
                                    }
                                });
                            });
                        } else {
                            if (_.last(product.attributeMap) === activeAttrID) {
                                def.resolve(true);
                            }
                        }
                    } else {
                        if (_.last(product.attributeMap) === activeAttrID) {
                            def.resolve(true);
                        }
                    }
                });
                return def.promise;
            }

            function setOptionExclusionsAsync(product, attrID, exclusions) {
                var def = $q.defer();
                var deletedAttrs = [];
                var attribute = _.findWhere(product.attributes, { attrID: attrID });
                var allExclude = [];

                _.each(exclusions, function (exc) {
                    _.each(exc, function (optID) {
                        allExclude.push(optID);
                        product.excludedOptions.push(optID);
                        _.each(product.selectedOptions, function (selectedOptID) {
                            if (_.contains(allExclude, selectedOptID)) {
                                getAttributeFromOption(product, selectedOptID).then(function (actAttrID) {
                                    if (actAttrID > 0 && _.indexOf(deletedAttrs, actAttrID) === -1) {
                                        delete product.selectedOptions[actAttrID];
                                        deletedAttrs.push(actAttrID);
                                    }
                                    def.resolve(deletedAttrs);
                                });
                            } else {
                                def.resolve(deletedAttrs);
                            }
                        });
                    });
                });

                attribute.filteredOptions = _.filter(attribute.options, function (opt) {
                    return !_.contains(product.excludedOptions, opt.ID);
                });

                return def.promise;
            }

            function getAttributeFromOption(product, optionID) {
                var def = $q.defer();
                _.each(product.optionMap, function (options, attrID) {
                    if (_.contains(options, optionID)) {
                        def.resolve(parseInt(attrID));
                    }
                });
                return def.promise;
            }

            $scope.checkRelatedFormats = function (product, format) {
                if (!format.relatedFormats) {
                    return true;
                }
                $scope.relatedFormats = [];
                _.each(format.relatedFormats, function (item) {
                    $scope.relatedFormats.push({ ID: item.formatID, typeID: item.typeID });
                });
            };

            $scope.filterRelatedFormats = function () {
                _.each($scope.complexGroups.slice(1), function (group) {
                    if (group.selectedProduct) {
                        if ($scope.complexGroups[0].selectedProduct.data.formats.length === 1) {
                            group.selectedProduct.data.relatedFormats = _.clone(group.selectedProduct.data.formats);
                        } else {
                            group.selectedProduct.data.relatedFormats = $filter('ids')(group.selectedProduct.data.formats, $scope.relatedFormats);
                        }
                    }
                });
            };

            $scope.selectDefaultFormats = function () {
                var def = $q.defer();
                _.each($scope.complexGroups.slice(1), function (group) {
                    if (!group.selectedProduct) {
                        return true;
                    }

                    var productData = group.selectedProduct.data;
                    var currentFormat = productData.currentFormat;
                    var find = -1;

                    if (!!currentFormat) {
                        find = _.findIndex($scope.relatedFormats, { ID: currentFormat.ID, typeID: productData.info.typeID });
                    }

                    if (find === -1) {
                        if (!angular.isDefined(productData.relatedFormats) || productData.relatedFormats.length === 0) {
                            productData.currentFormat = null;
                            return true;
                        } else {
                            var searchFormat = filterFormats(productData.formats, $scope.relatedFormats)[0];
                            if (searchFormat) {
                                productData.currentFormat = searchFormat;
                                if (!!searchFormat.custom) {
                                    productData.currentFormat.customWidth = searchFormat.minWidth - searchFormat.slope * 2;
                                    productData.currentFormat.customHeight = searchFormat.minHeight - searchFormat.slope * 2;
                                }
                            }

                            if (!productData.currentFormat) {
                                def.reject({ 'info': 'select another format' });
                                Notification.error($filter('translate')('not_related_format_for_product') + ' - ' + productData.info.typeName);
                            }
                        }
                    } else {
                        // if is in related formats so again assign it than if we change product select can update
                        var idx = _.findIndex(productData.relatedFormats, { ID: currentFormat.ID });
                        if (idx > -1) {
                            productData.currentFormat = productData.relatedFormats[idx];
                        }
                    }

                    $scope.checkFormatExclusions(productData);
                    setExclusionsAsync(productData).then(function (exclusionEnd) {
                        if (exclusionEnd) {
                            $scope.selectDefaultOptions(productData);
                        }
                    });
                });
                def.resolve();
    
                return def.promise;
            };
    
            function filterFormats(input, ids) {
    
                var result = [];
    
                _.each(input, function (item) {
                    var idx = _.findIndex(ids, {ID: item.ID});
                    if (idx > -1) {
                        result.push(item);
                    }
                });
                return result;
    
            }
    
            $scope.checkFormatExclusions = function (product) {
                if (!product.currentFormat) {
                    return false;
                }
                product.formatExcluded = [];
                _.each(product.attributes, function (attribute, attrIdx) {
                    _.each(attribute.options, function (option, optIdx) {
                        if (option && option.formats) {
                            if (!_.contains(option.formats, product.currentFormat.ID)) {
                                product.formatExcluded.push(option.ID);
                                if (product.selectedOptions[attribute.attrID] === option.ID) {
                                    delete product.selectedOptions[attribute.attrID];
                                }
                            }
                        }
                    });
                });
    
            };
    
            var debounceTimeout;
            $scope.getVolumesDebounced = function () {
                if (debounceTimeout) {
                    $timeout.cancel(debounceTimeout);
                }
    
                debounceTimeout = $timeout(function () {
                    $scope.getVolumes($scope.productItem.amount);
                }, 1500);
            };
    
            $scope.selectPagesHandler = function (product, pages) {
                if (pageTimeout) {
                    $timeout.cancel(pageTimeout);
                }
    
                pageTimeout = $timeout(function () {
                    $scope.selectPages(product, pages);
                }, 1500);
            };
    
            var wingtipTimeout;
            $scope.changeWingtip = function (format, field) {
                if (wingtipTimeout) {
                    $timeout.cancel(wingtipTimeout);
                }
                wingtipTimeout = $timeout(function () {
                    var val = format[field];
                    var min = format[field + 'Min'];
                    if (val < min) {
                        Notification.info($filter('translate')('Minimal wingtip is ') + ' ' + min);
                        format[field] = min;
                    }
                }, 1200);
            };
    
            $scope.selectPages = function (product, pages) {
    
                var stopSelect;
    
                pages = Number(pages);
    
                if (product.pages[0] && product.pages[0].pages) {
    
                    product.currentPages = pages;
    
                    $scope.calcProductThickness(product);
                    setExclusionsAsync(product).then(function (exclusionEnd) {
                        if (exclusionEnd) {
                            _.each(product.attrPages, function (oneAttrPage, attrID) {
                                if (product.currentPages < oneAttrPage) {
                                    product.attrPages[attrID] = product.currentPages;
                                }
                            });
    
                            $scope.getVolumes($scope.productItem.amount);
                        }
                    });
    
                } else {
                    if (product.pages[0] && product.pages[0].step !== null) {
                        var step = Number(product.pages[0].step);
                    }
    
                    if (angular.isDefined(stopSelect)) {
                        $timeout.cancel(stopSelect);
                        stopSelect = undefined;
                    }
    
                    stopSelect = $timeout(function () {
                        var maxPages = $scope.getMaximumThickness(product);
                        var minPages = $scope.getMinimumThickness(product);
    
                        if (product.pages[0]) {
                            if (parseInt(product.pages[0].maxPages) > 0 && maxPages > parseInt(product.pages[0].maxPages)) {
                                maxPages = parseInt(product.pages[0].maxPages);
                            }
    
                            if (product.pages[0].minPages !== null && minPages < parseInt(product.pages[0].minPages)) {
                                minPages = parseInt(product.pages[0].minPages);
                            }
    
                            if (product.pages[0].step !== null) {
                                if (pages % step !== 0) {
                                    if ((pages % step) > (step / 2)) {
                                        pages = pages + (step - (pages % step));
                                    } else {
                                        pages -= pages % step;
                                    }
                                }
                            }
                        }
    
                        if (pages > maxPages) {
                            Notification.info($filter('translate')('maximum_number_of_pages') + ' ' + maxPages);
                            product.currentPages = maxPages;
                            pages = maxPages;
                        } else if (pages < minPages) {
                            Notification.info($filter('translate')('minimum_number_of_pages') + ' ' + minPages);
                            product.currentPages = minPages;
                            pages = minPages;
                        } else if (pages === undefined) {
                            Notification.info($filter('translate')('range_of_pages') + ' ' + minPages + ' - ' + maxPages);
                        } else {
                            product.currentPages = pages;
                        }
    
                        $scope.calcProductThickness(product);
    
                        setExclusionsAsync(product).then(function (exclusionEnd) {
    
                            if (exclusionEnd) {
                                _.each(product.attrPages, function (oneAttrPage, attrID) {
                                    if (product.currentPages < oneAttrPage) {
                                        product.attrPages[attrID] = product.currentPages;
                                    }
                                });
    
                                if (pages <= maxPages && pages >= minPages && pages !== undefined) {
    
                                    $scope.getVolumes($scope.productItem.amount);
                                }
                            }
    
                        });
    
                    }, 1500);
                }
            };
    
            $scope.selectPagesOption = function (product) {
                var pages = Number(product.currentPages);
            };
    
            $scope.calcProductThickness = function (product) {
    
                var sheets = product.currentPages / 2;
                if (!_.keys(product.thickness.values).length) {
                    product.thickness.current = null;
                    return true;
                }
                var doublePage = !!product.pages[0].doublePage;
                if (doublePage) {
                    sheets /= 2;
                }
    
                var value = _.sum(_.values(product.thickness.values));
                product.thickness.current = sheets * value;
                return true;
            };
    
            $scope.getMinimumThickness = function (product) {
                if (product === undefined) {
                    return false;
                }
                if (!_.keys(product.thickness.values).length || !product.thickness.min) {
                    return product.pages[0].minPages || 0;
                }
                var value = _.sum(_.values(product.thickness.values));
                var sheets = product.thickness.min / value;
                var pages = Math.ceil(sheets) * 2;
                var doublePage = !!product.pages[0].doublePage;
                if (doublePage) {
                    pages *= 2;
                }
    
                if (!!product.pages[0].step) {
                    var modulo = pages % product.pages[0].step;
                    if (modulo) {
                        pages += product.pages[0].step - modulo;
                    }
                }
    
                if (product.currentPages < pages) {
                    $scope.selectPages(product, pages);
                }
                return pages;
            };
    
            $scope.getMaximumThickness = function (product) {
                if (product === undefined) {
                    return false;
                }
                if (!_.keys(product.thickness.values).length || !product.thickness.max) {
                    return product.pages[0].maxPages || 9999999;
                }
                var value = _.sum(_.values(product.thickness.values));
                var sheets = product.thickness.max / value;
                var pages = Math.floor(sheets) * 2;
                var doublePage = !!product.pages[0].doublePage;
    
                if (doublePage) {
                    pages *= 2;
                }
    
                if (!!product.pages[0].step) {
                    var modulo = pages % product.pages[0].step;
                    if (modulo) {
                        pages -= modulo;
                    }
                }
    
                if (product.currentPages > pages) {
                    $scope.selectPages(product, pages);
                }
    
                return pages;
            };
    
            $scope.thicknessFilter = function (product) {
                var minValue = $scope.getMinimumThickness(product);
                var maxValue = $scope.getMaximumThickness(product);
    
                return function predicateFunc(item) {
                    return minValue <= item.pages && item.pages <= maxValue;
                };
    
            };
    
            $scope.selectDefaultOptions = function (product) {
                var currentCalcProduct = getCurrentCalcProduct(product.info);
    
                _.each(product.attributes, function (item) {
    
                    if (!product.selectedOptions[item.attrID]) {
                        var currentCalcAttr = null;
                        if (currentCalcProduct) {
                            currentCalcAttr = _.findWhere(currentCalcProduct.attributes, {attrID: item.attrID});
                        }
    
                        var tmp;
                        _.each(item.options, function (option, idx) {
                            if (currentCalcAttr) {
                                if (currentCalcAttr.optID !== option.ID) {
                                    return true;
                                }
                                if (currentCalcAttr.attrPages) {
                                    product.attrPages[item.attrID] = currentCalcAttr.attrPages;
                                }
                            }
    
                            if (!_.contains(product.excludedOptions, option.ID)) {
                                tmp = option;
                                return false;
                            } else {
                                console.log('Opcja wykluczona', option);
                            }
                        });
                        $scope.selectOption(product, item.attrID, tmp);
                    }
                });
            };
    
            $scope.selectOption = function (product, attrID, option) {
    
                var itemExist = true;
    
                if (option === undefined) {
                    itemExist = false;
                    var optID = product.selectedOptions[attrID];
    
                    option = getOption(product, optID);
    
                    if (option === undefined) {
                        return false;
                    }
                }
                if(product.attributes[product.attributeMap.indexOf(attrID)].multipleOptionsMax>1){
                    product.selectedOptions[attrID] = [parseInt(option.ID)];
                }else{
                    product.selectedOptions[attrID] = parseInt(option.ID);
                }
    
                setRangePages(product, attrID);
    
                if (product.thickness.minAttr === attrID) {
                    product.thickness.min = null;
                    product.thickness.minAttr = null;
                }
    
                if (product.thickness.maxAttr === attrID) {
                    product.thickness.max = null;
                    product.thickness.maxAttr = null;
                }
    
                /**
                 * @param {Object} item
                 * @param {number|null} item.minThickness
                 * @param {number|null} item.maxThickness
                 * @param {number} item.sizePage
                 */
                if (Number(option.minThickness) > 0 && (Number(option.minThickness) > product.thickness.min || option.minThickness === null)) {
                    product.thickness.min = option.minThickness;
                    product.thickness.minAttr = attrID;
                }
    
                if (Number(option.maxThickness) > 0 && (Number(option.maxThickness) < product.thickness.max || product.thickness.max === null)) {
    
                    product.thickness.max = option.maxThickness;
                    product.thickness.maxAttr = attrID;
                }
    
                product.thickness.values[attrID] = option.sizePage;
    
                if (product.pages.length) {
                    $scope.calcProductThickness(product);
                    $scope.getMinimumThickness(product);
                    $scope.getMaximumThickness(product);
                }
    
                setExclusionsAsync(product).then(function (exclusionEnd) {
    
                    if (exclusionEnd) {
                        $scope.selectDefaultOptions(product);
                        if (!itemExist) {
                            $scope.getVolumes($scope.productItem.amount);
                        }
                    }
    
                });
    
            };
    
            var setRangePages = function (product, attrID) {
                var idx = _.findIndex(product.attributes, {attrID: attrID});
                if (idx > -1) {
    
                    var actOptID = product.selectedOptions[attrID];
    
                    var optionIndex = _.findIndex(product.attributes[idx].filteredOptions, {ID: actOptID});
    
                    if (optionIndex > -1) {
                        if (product.attributes[idx].filteredOptions[optionIndex].emptyChoice === true) {
                            product.attributes[idx].emptyChoice = true;
                        } else {
                            product.attributes[idx].emptyChoice = false;
                        }
                    }
    
                    if (product.attributes[idx].minPages !== null) {
                        if (!product.attrPages[attrID]) {
                            product.attrPages[attrID] = product.attributes[idx].minPages;
                        }
                    }
                } else {
                    console.log('Something went wrong :/');
                }
            };
    
            var getOption = function (product, optID) {
                var item;
                _.each(product.attributes, function (attribute) {
                    var idx = _.findIndex(attribute.options, {ID: optID});
                    if (idx > -1) {
                        item = attribute.options[idx];
                        return false;
                    }
                });

                return item;
            };
    
            $scope.countAttrNotExcludedOptions = function (product, attr) {
                var count = 0;
                _.each(attr.options, function (option) {
                    if (!_.contains(product.excludedOptions, option.ID)) {
                        count++;
                    }
                });
                return count;
            };
    
            $scope.setExclusions = function (product) {
                product.excludedOptions = _.clone(product.formatExcluded);
                _.each(product.attributes, function (attribute) {
                    attribute.filteredOptions = _.clone(attribute.options, true);
                });
    
                _.each(product.selectedOptions, function (optID, attrID) {
    
                    if (!optID) {
                        return false;
                    }
                    var item = getOption(product, optID);
                    if (item.exclusions) {
                        $scope.setOptionExclusions(product, item.exclusions);
                    }
                });
            };
    
            $scope.setOptionExclusions = function (product, exclusions) {
    
                _.each(product.attributes, function (attribute) {
    
                    if (exclusions[attribute.attrID]) {
    
                        _.each(attribute.options, function (option) {
    
                            if (_.contains(exclusions[attribute.attrID], option.ID)) {
    
                                product.excludedOptions.push(option.ID);
    
                                if (product.selectedOptions[attribute.attrID] === option.ID) {
                                    delete product.selectedOptions[attribute.attrID];
                                }
                            }
                        });
    
                    }
                });
    
                _.each(product.attributes, function (attribute) {
                    attribute.filteredOptions = _.filter(attribute.options, function (opt) {
                        return !_.contains(product.excludedOptions, opt.ID);
                    });
                });
            };
    
            $scope.goToProducts = function () {
                $scope.currentGroup = false;
                $scope.currentType = false;
            };
    
            $scope.goToTypes = function () {
                if (typeOfResource.type === 'order') {
                    $state.go('create-order-types', {groupID: $scope.currentGroup.ID});
                } else if (typeOfResource.type === 'offer') {
                    $state.go('create-offer-types', {groupID: $scope.currentGroup.ID});
                }
    
            };
    
            $scope.filterRealisationTime = function (rt) {
                return rt.active ? 1 : 0;
            };
    
            $scope.getVolumes = function (amount) {
                $scope.volumes = {};
                $scope.calculation = {};
    
                var preparedProduct = getPreparedProduct(amount);
                CalculateService = new PsCalculateService(preparedProduct.groupID, preparedProduct.typeID);
                CalculateService.getVolumes(preparedProduct).then(function (data) {
    
                    HelpersService.showStandardMessages(data);
    
                    $scope.realisationTimes = data.realisationTimes;
    
                    if(!$scope.productItem.realisationTime){
                        $scope.productItem.realisationTime=data.realisationTimes[0].ID;
                    }
    
                    $scope.changeRealizationTime($scope.productItem);
    
                    if ($scope.productItem.volume !== undefined && $scope.productItem.volume > 0) {
                        $scope.calculate($scope.productItem.amount, $scope.productItem.volume);
                    }
    
                    if (_.isEmpty($scope.printTypes)) {
                        CalculateService.possibleTechnologies(preparedProduct).then(function (data) {
                            $scope.printTypes = data;
                        });
                    }
    
                }, function (data) {
                    HelpersService.showStandardMessages(data);
                    Notification.error($filter('translate')('error'));
                });
            };
    
            $scope.updatePrintTypes = function (product) {
                var preparedProduct = getPreparedProduct(0);
                var selectedPrintType=product.data.printType;
                CalculateService.possibleTechnologies(preparedProduct).then(function (data) {
                    $scope.printTypes = data;
                    if(selectedPrintType){
                        product.data.printType=_.findWhere($scope.printTypes[product.typeID],{printTypeID:selectedPrintType.printTypeID});
                    }
                });
            };
    
            function searchComplexGroup(typeID) {
                var def = $q.defer();
    
                _.each($scope.complexGroups, function (complexGroup) {
    
                    if (complexGroup.selectedProduct.typeID === typeID) {
                        def.resolve(complexGroup);
                    }
    
                });
    
                return def.promise;
            }
    
            $scope.showVolumes = function (data) {
                $scope.volumes = data.volumes;
            };
    
            $scope.calculate = function (amount, volume) {
                $scope.calculation = {};
                $scope.calculationInfo = [];
                var preparedProduct = getPreparedProduct(amount, volume);
    
                CalculateService = new PsCalculateService(preparedProduct.groupID, preparedProduct.typeID);
                CalculateService.calculate(preparedProduct).then(function (data) {
                    var volumes = _.findWhere(data.realisationTimes[$scope.type.ID], {ID: preparedProduct.products[0].realisationTime}).volumes;
                    var volumeItem = _.findWhere(volumes, {volume: parseInt(volume)});
                    if (volumeItem) {
                        data.calculation.price = volumeItem.price;
                    }
                    $scope.showCalculation(data);
                    $scope.countGrossPrice(data.calculation, $scope.sellerForm);
                    countPaperPrice(data);
                    checkPosiblePrintTypes(data);
                    showExpense(data.calculation);
                    showProfit(data.calculation);
                    HelpersService.showStandardMessages(data);
                    Notification.success($filter('translate')('success'));
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                });
            };
    
            function showExpense(calculation) {
    
                if (typeof calculation.expense === 'string') {
                    calculation.expense = (parseFloat(calculation.expense.replace('.', ',')) / 100).toFixed(2) + ''.replace('.', ',');
                } else {
                    calculation.expense = (calculation.expense / 100).toFixed(2).replace('.', ',');
                }
    
            }
    
            function showProfit(calculation) {
    
                var tmpPrice = 0;
                if (typeof calculation.price === 'string') {
                    calculation.price = calculation.price.replace(',', '.');
                    tmpPrice = calculation.price;
                } else {
                    tmpPrice = calculation.price;
                }
    
                var tmpExpense = 0;
                if (typeof calculation.expense === 'string') {
                    calculation.expense = calculation.expense.replace(',', '.');
                    tmpExpense = calculation.expense;
                } else {
                    tmpExpense = calculation.expense;
                }
    
                calculation.profit = (calculation.price - calculation.expense).toFixed(2).replace('.', ',');
    
            }
    
            $scope.saveCalculation = function (amount, volume) {
                var preparedProduct = getPreparedProduct(amount, volume);
    
                preparedProduct.price = $scope.sellerForm.price;
                preparedProduct.name = $scope.productItem.name;
                preparedProduct.files = $scope.sellerForm.files;
                preparedProduct.updateReason = $scope.sellerForm.updateReason;
    
                if($scope.currentMultiOfferVolumes.length > 0 && $scope.currentCalc){
                    preparedProduct.updateMultiOfferCalc = $scope.currentCalc.ID;
                }
    
                if (typeOfResource.type === 'offer') {
                    preparedProduct.isOffer = 1;
                }
    
                preparedProduct.isSeller = 1;
                if (orderID) {
                    preparedProduct.orderID = orderID;
                }
                if (currentProductID) {
                    preparedProduct.productID = currentProductID;
                }
                if ($scope.currentCalc) {
                    preparedProduct.baseID = $scope.currentCalc.baseID;
                }
    
                if ($state.params.customProductID) {
                    preparedProduct.customProductID = $state.params.customProductID;
                }
    
                CalculateService = new PsCalculateService(preparedProduct.groupID, preparedProduct.typeID);
                CalculateService.saveCalculation(preparedProduct).then(function (data) {
                    Notification.success($filter('translate')('success'));
                    var userID = $scope.currentUser ? $scope.currentUser.ID : null;
    
                    console.log(typeOfResource);

                    if (!$scope.currentMultiOfferVolumes.length > 0 && !$scope.currentCalc) {
                        $scope.leaveCalc(data);
                    } else {
                        if ($scope.customProduct === false) {
                            $scope.edit(data.calcID);
                        } else {
                            $scope.leaveCalc(data);
                        }
                    }
    
                }, function (data) {
                    console.log(data);
                    Notification.error($filter('translate')('error'));
                });
            };
    
            function getPreparedProduct(amount, volume) {
                var orderData = OrderDataService.getLastOrder();
                var newItem = {};

                newItem.amount = amount;
                if (volume !== undefined) {
                    newItem.volume = volume;
                }
                newItem.groupID = $scope.currentGroup.ID;
                newItem.typeID = $scope.currentType.ID;
                if (parseInt(userID) > 0) {
                    newItem.userID = parseInt(userID);
                }
                newItem.taxID = $scope.productItem.taxID;
                newItem.products = [];
                newItem.currency = orderData.currency;
                _.each($scope.complexGroups, function (complexGroup) {
                    var product = complexGroup.selectedProduct.data;
                    var newProduct = {};
                    newItem.products.push(newProduct);
                    newProduct.groupID = product.info.groupID;
                    newProduct.typeID = product.info.typeID;
                    newProduct.name = product.info.typeName;
                    newProduct.realisationTime = $scope.productItem.realisationTime;

                    newProduct.formatID = product.currentFormat.ID;

                    if (complexGroup.selectedProduct.data.currentFormat.wingtipFront) {
                        newProduct.wingtipFront = complexGroup.selectedProduct.data.currentFormat.wingtipFront;
                    }

                    if (complexGroup.selectedProduct.data.currentFormat.wingtipBack) {
                        newProduct.wingtipBack = complexGroup.selectedProduct.data.currentFormat.wingtipBack;
                    }

                    if (product.printType) {
                        newProduct.printTypeID = product.printType.ID;
                    }

                    if (product.workspace) {
                        newProduct.workspaceID = product.workspace.ID;
                    }

                    if (!product.currentFormat.custom) {
                        newProduct.width = product.currentFormat.width;
                        newProduct.height = product.currentFormat.height;
                    } else {
                        newProduct.width = product.currentFormat.customWidth + product.currentFormat.slope * 2;
                        newProduct.height = product.currentFormat.customHeight + product.currentFormat.slope * 2;
                    }

                    if (product.currentPages) {
                        newProduct.pages = product.currentPages;
                    } else {
                        newProduct.pages = 2;
                    }

                    if (product.useForSheet) {
                        newProduct.useForSheet = product.useForSheet;
                    } else {
                        newProduct.useForSheet = null;
                    }

                    newProduct.options = [];
                    _.each(product.info.data.attributes, function (attr) {
                        if (attr.attrID < 0) {
                            return;
                        }
                        var optID = product.selectedOptions[attr.attrID];
                        var attrID = attr.attrID;

                        if (optID) {
                            var optIDS = _.isArray(optID) ? optID : [optID];
                            _.each(optIDS, function(id) {
                                newProduct.options.push({
                                    attrID: parseInt(attrID),
                                    optID: id
                                });
                            });
                        }
                    });

                    newProduct.specialAttributes = _.filter(complexGroup.specialAttributes, function (one) {
                        if (one.saved === true) {
                            return one;
                        }
                    });

                    newProduct.attrPages = product.attrPages;
                });

                return newItem;
            }
    
            $scope.selectAttrPages = function (complexProduct, attrID) {
    
                var stopSelectAttr;
    
                if (angular.isDefined(stopSelectAttr)) {
                    $timeout.cancel(stopSelectAttr);
                    stopSelectAttr = undefined;
                }
    
                stopSelectAttr = $timeout(function () {
    
                    if (complexProduct.selectedProduct.data.attrPages[attrID] <= 0) {
                        complexProduct.selectedProduct.data.attrPages[attrID] = 0;
                    }
    
                    var attrIdx = _.findIndex(complexProduct.selectedProduct.data.attributes, {attrID: parseInt(attrID)});
    
                    if (attrIdx > -1) {
                        var attribute = complexProduct.selectedProduct.data.attributes[attrIdx];
    
                        var maxPages = attribute.maxPages;
                        if (maxPages === null) {
                            maxPages = complexProduct.selectedProduct.data.currentPages;
                        }
    
                        if (complexProduct.selectedProduct.data.attrPages[attrID] > maxPages) {
                            Notification.info($filter('translate')('maximum_number_of_pages') + ' ' + maxPages);
                            complexProduct.selectedProduct.data.attrPages[attrID] = maxPages;
                            return;
                        }
    
                        if (complexProduct.selectedProduct.data.attrPages[attrID] < attribute.minPages) {
                            Notification.info($filter('translate')('minimum_number_of_pages') + ' ' + attribute.minPages);
                            complexProduct.selectedProduct.data.attrPages[attrID] = attribute.minPages;
                            return;
                        }
                    }
    
                }, 1500);
    
            };
    
            $scope.showCalculation = function (data) {
                $scope.calculation = data.calculation;
                $scope.sellerForm.price = data.calculation.price;
                $scope.sellerForm.priceBrutto = data.calculation.priceBrutto;
                $scope.calculationInfo = data.info;
                $scope.calculationProducts=data.products;
            };
    
            $scope.showImposition = function (workspace, targetID) {
                HelpersService.showImposition(workspace, workspace.areaPerSheetForStandardResult.formatWidth, workspace.areaPerSheetForStandardResult.formatHeight, targetID);
            };
    
            $scope.addFile = function () {
                if (!$scope.sellerForm.files) {
                    $scope.sellerForm.files = [];
                }
    
                $scope.sellerForm.files.push({'name': ''});
            };
    
            $scope.addSpecialAttribute = function (complexGroup) {
    
                if (complexGroup.addMode) {
                    return;
                }
    
                complexGroup.addMode = true;
    
                if (complexGroup.specialAttributes === undefined) {
                    complexGroup.specialAttributes = [];
                }
                complexGroup.specialAttributes.push({type:$scope.specialAttributeTypes[0].type});
            };
    
            $scope.priceSync = function (attribute, useCase) {
                var sourceValue = useCase === 1 ? attribute.price:attribute.grossPrice;
                if (sourceValue === 'string') {
                    sourceValue = sourceValue.replace(',', '.');
                }
                var defaultTax = $scope.calculation && $scope.calculation.tax && $scope.calculation ?
                    $scope.calculation.tax.value :
                    $rootScope.currentDomain.taxes.find(function (tax) {
                        return tax.default;
                    }).value;
                var tax = 1 + (defaultTax / 100);
                var format = function (num) {
                    return parseFloat(num).toFixed(2);
                };
                if (useCase === 1) {
                    attribute.grossPrice = format(sourceValue * tax);
                } else if (useCase === 2) {
                    attribute.price = format(sourceValue / tax);
                }
            };
    
            $scope.saveSpecialAttribute = function (complexGroup, specialAttribute) {
    
                if (_.isUndefined(specialAttribute.price) || _.isEmpty(specialAttribute.price)) {
                    specialAttribute.priceError = true;
                    Notification.error($filter('translate')('select_all_required_fields'));
                    return false;
                } else {
                    specialAttribute.priceError = false;
                }
    
                if (_.isUndefined(specialAttribute.name) || _.isEmpty(specialAttribute.name)) {
                    specialAttribute.nameError = true;
                    Notification.error($filter('translate')('select_all_required_fields'));
                    return false;
                } else {
                    specialAttribute.nameError = false;
                }
    
                if (_.isUndefined(specialAttribute.type) || parseInt(specialAttribute.type) <= 0) {
                    specialAttribute.typeError = true;
                    Notification.error($filter('translate')('select_all_required_fields'));
                    return false;
                } else {
                    specialAttribute.typeError = false;
                }
    
                specialAttribute.saved = true;
                complexGroup.addMode = false;
            };
    
            $scope.removeSpecialAttribute = function (complexGroup, index) {
                complexGroup.specialAttributes.splice(index, 1);
            };
    
            $scope.getSpecialAttributePlaceholder = function (specialAttribute) {
                if (specialAttribute.type === 1) {
                    return '1' + $filter('translate')('piece_symbol') + ' ' + $filter('translate')('grams');
                } else if (specialAttribute.type === 2) {
                    return 'g / m2';
                } else {
                    return $filter('translate')('weight');
                }
            };
    
            $scope.filterByThickness = function (product) {
    
                var exclusions = {};
    
                _.each(product.attributes, function (attribute) {
    
                    exclusions[attribute.attrID] = [];
                    var idx;
                    _.each(attribute.options, function (option) {
    
                        if (angular.isDefined(option.maxThickness) && Number(option.maxThickness) > 0) {
    
                            if (product.thickness.current > option.maxThickness) {
    
                                idx = product.excludedOptions.indexOf(option.ID);
                                if (idx === -1) {
                                    exclusions[attribute.attrID].push(option.ID);
                                }
    
                            }
                        }
    
                        if (angular.isDefined(option.minThickness) && Number(option.minThickness) > 0) {
    
                            if (product.thickness.current < option.minThickness) {
    
                                idx = product.excludedOptions.indexOf(option.ID);
                                if (idx === -1) {
                                    exclusions[attribute.attrID].push(option.ID);
                                }
    
                            }
    
                        }
    
                    });
    
                });
    
                return exclusions;
            };
    
            $scope.filterByOptionsPages = function (product) {
    
                var exclusions = {};
    
                _.each(product.attributes, function (attribute) {
    
                    exclusions[attribute.attrID] = [];
    
                    _.each(attribute.options, function (option) {
    
                        /**
                         * @param {number} option.maxPages
                         */
    
                        if (product.currentPages && angular.isDefined(option.maxPages) && Number(option.maxPages) > 0) {
    
                            if (product.currentPages > option.maxPages) {
    
                                idx = product.excludedOptions.indexOf(option.ID);
                                if (idx === -1) {
                                    exclusions[attribute.attrID].push(option.ID);
                                }
    
                            }
                        }
    
                        if (product.currentPages && angular.isDefined(option.minPages) && Number(option.minPages) > 0) {
    
                            if (product.currentPages < option.minPages) {
    
                                var idx = product.excludedOptions.indexOf(option.ID);
    
                                if (idx === -1) {
                                    exclusions[attribute.attrID].push(option.ID);
                                }
    
                            }
    
                        }
    
                    });
    
                });
    
                return exclusions;
            };
    
            function checkAttrSelectAsync(product,deletedAttrs) {
                var def = $q.defer();
    
                _.each(product.attributes, function (attribute) {
                    if (_.contains(deletedAttrs, attribute.attrID)) {
                        if (product.selectedOptions[attribute.attrID]) {
                            var firstFilteredOption = _.first(attribute.filteredOptions);
                            if (firstFilteredOption) {
                                product.selectedOptions[attribute.attrID] = firstFilteredOption.ID;
                            }
                        }
                    }
    
                    if (_.last(product.attributeMap) === attribute.attrID) {
                        def.resolve(true);
                    }
    
                });
    
                return def.promise;
            }
    
            function countPaperPrice(data) {
    
                var paperPrice = 0;
                _.each(data.info, function (info) {
                    var printType = _.findWhere(info.printTypes, {printTypeID: info.selectedPrintType.printTypeID});
                    var workspace = _.findWhere(printType.workspaces, {workspaceID: info.selectedPrintType.workspaceID});
                    var paperAttr = _.find(workspace.attrs, function (attr) {
                        return attr.calcInfo.paperPriceKG;
                    });
                    if (paperAttr) {
                        paperPrice += paperAttr.attrPrice;
                    }
    
                });
    
                $scope.paperPrice = (Math.round(paperPrice) / 100).toFixed(2);
            }
    
            function checkPosiblePrintTypes(data) {
                var invalidPT = [];
                _.each(data.info, function (info) {
                    _.each(info.printTypes, function (pt) {
                        if (pt.workspaces.length===0) {
                            invalidPT.push(pt.name);
                        }
                    });
                });
                if(invalidPT.length>0){
                    Notification.warning($filter('translate')('product_format_larger_than_print_type') + ' ' + invalidPT.join(', '));
                }
            }
    
            $scope.selectCustomFormat = function (complexProduct) {
    
                complexProduct.selectedProduct.data.currentFormat.customHeight = Number(complexProduct.selectedProduct.data.currentFormat.customHeight);
                complexProduct.selectedProduct.data.currentFormat.customWidth = Number(complexProduct.selectedProduct.data.currentFormat.customWidth);
    
                if (angular.isDefined(stopSelectCustomFormat)) {
                    $timeout.cancel(stopSelectCustomFormat);
                    stopSelectCustomFormat = undefined;
                }
    
                stopSelectCustomFormat = $timeout(function () {
    
                    // check maximal and minimal customSize
                    var minHeight = complexProduct.selectedProduct.data.currentFormat.minHeight - complexProduct.selectedProduct.data.currentFormat.slope * 2;
                    var minWidth = complexProduct.selectedProduct.data.currentFormat.minWidth - complexProduct.selectedProduct.data.currentFormat.slope * 2;
    
                    var maxHeight = complexProduct.selectedProduct.data.currentFormat.maxHeight - complexProduct.selectedProduct.data.currentFormat.slope * 2;
                    var maxWidth = complexProduct.selectedProduct.data.currentFormat.maxWidth - complexProduct.selectedProduct.data.currentFormat.slope * 2;
    
                    var valueIsCorrect = true;
    
                    if (complexProduct.selectedProduct.data.currentFormat.customHeight > maxHeight) {
                        Notification.info($filter('translate')('value_greater_than_maximum') + ' ' + maxHeight);
                        complexProduct.selectedProduct.data.currentFormat.customHeight = maxHeight;
                        valueIsCorrect = false;
                    }
    
                    if (complexProduct.selectedProduct.data.currentFormat.customHeight < minHeight) {
                        Notification.info($filter('translate')('value_lower_than_minimum') + ' ' + minHeight);
                        complexProduct.selectedProduct.data.currentFormat.customHeight = minHeight;
                        valueIsCorrect = false;
                    }
    
                    if (complexProduct.selectedProduct.data.currentFormat.customWidth > maxWidth) {
                        Notification.info($filter('translate')('value_greater_than_maximum') + ' ' + maxWidth);
                        complexProduct.selectedProduct.data.currentFormat.customWidth = maxWidth;
                        valueIsCorrect = false;
                    }
    
                    if (complexProduct.selectedProduct.data.currentFormat.customWidth < minWidth) {
                        Notification.info($filter('translate')('value_lower_than_minimum') + ' ' + minWidth);
                        complexProduct.selectedProduct.data.currentFormat.customWidth = minWidth;
                        valueIsCorrect = false;
                    }
    
                    if (valueIsCorrect) {
                        $scope.getVolumes($scope.productItem.amount);
                    }
    
                }, 1500);
            };
    
            $scope.countGrossPrice = function (calculation, sellerForm) {
    
                var tmpPrice = 0;
                if (typeof calculation.price === 'string') {
                    calculation.price = calculation.price.replace(',', '.');
                }
                if (typeof sellerForm.price === 'string') {
                    sellerForm.price = sellerForm.price.replace(',', '.');
                    tmpPrice = sellerForm.price;
                } else {
                    tmpPrice = sellerForm.price;
                }
    
                if( calculation.price !== sellerForm.price) {
                    $scope.priceUpdated = true;
                }
    
                if (tmpPrice > 0) {
                    sellerForm.priceBrutto = calculation.priceBrutto = (tmpPrice * (1 + (calculation.tax.value / 100))).toFixed(2).replace('.', ',');
                    calculation.price = parseFloat(tmpPrice).toFixed(2);
                }
    
            };
    
            $scope.countNetPrice = function (calculation, sellerForm) {
    
                var tmpPrice = 0;
    
                if (typeof calculation.price === 'string') {
                    calculation.priceBrutto = calculation.priceBrutto.replace(',', '.');
                }
    
                if (typeof sellerForm.priceBrutto === 'string') {
                    sellerForm.priceBrutto = sellerForm.priceBrutto.replace(',', '.');
                    tmpPrice = sellerForm.priceBrutto;
                } else {
                    tmpPrice = sellerForm.priceBrutto;
                }
    
                if( calculation.priceBrutto !== sellerForm.priceBrutto) {
                    $scope.priceUpdated = true;
                }
    
                if (tmpPrice > 0) {
                    sellerForm.price = calculation.price = (tmpPrice / (1 + (calculation.tax.value / 100))).toFixed(2).replace('.', ',');
                    if (typeof tmpPrice === 'string') {
                        tmpPrice = tmpPrice.replace(',', '.');
                    }
                    calculation.priceBrutto = parseFloat(tmpPrice).toFixed(2);
                }
    
            };
    
            $scope.countProfit = function (calculation, sellerForm) {
                var tmpPrice = 0;
                if (typeof sellerForm.price === 'string') {
                    sellerForm.price = sellerForm.price.replace(',', '.');
                    tmpPrice = sellerForm.price;
                } else {
                    tmpPrice = sellerForm.price;
                }
    
                var tmpExpense = 0;
                if (typeof calculation.expense === 'string') {
                    calculation.expense = calculation.expense.replace(',', '.');
                    tmpExpense = calculation.expense;
                } else {
                    tmpExpense = calculation.expense;
                }
    
                calculation.profit = (sellerForm.price - calculation.expense).toFixed(2).replace('.', ',');
    
            };
    
            $scope.selectPrintType = function (complexGroup) {
                if( !complexGroup.selectedProduct.data.printType ) {
                    complexGroup.selectedProduct.data.workspace = null;
                    return;
                }
                var index = _.findIndex($scope.printTypes[complexGroup.selectedProduct.typeID], {ID: complexGroup.selectedProduct.data.printType.ID});
                if (index > -1) {
                    complexGroup.selectedProduct.data.printType.currentIndex = index;
                }
            };
    
            $scope.checkZeroValue = function (complexGroup) {
                if (complexGroup.selectedProduct.data.useForSheet <= 0) {
                    complexGroup.selectedProduct.data.useForSheet = null;
                    Notification.info($filter('translate')('value_lower_than_minimum') + ' ' + 1);
                }
            };
    
            $scope.changeAttrPrice = function (info, workspace, printType) {
    
                var newPrice = 0;
                _.each(workspace.attrs, function (attribute, index) {
                    if (typeof attribute.attrPriceFormatted === 'string') {
                        attribute.attrPriceFormatted = attribute.attrPriceFormatted.replace(',', '.');
                    }
                    newPrice += parseFloat(attribute.attrPriceFormatted);
    
                    if (workspace.attrs.length === (index + 1)) {
                        workspace.price = newPrice * 100;
                        if (workspace.workspaceID === info.selectedPrintType.workspaceID &&
                            printType.printTypeID === info.selectedPrintType.printTypeID) {
                            $scope.sellerForm.price = newPrice.toFixed(2);
                            $scope.countGrossPrice($scope.calculation, $scope.sellerForm);
                            $scope.countProfit($scope.calculation, $scope.sellerForm);
                        }
                    }
                });
    
            };
    
            $scope.isFoldMethod=function(optionInfo){
                if(optionInfo.workUnits.length>0){
                    return optionInfo.workUnits.indexOf('folds') > -1 || optionInfo.workUnits.indexOf('collectingFolds') > -1;
                }
                return optionInfo.priceFunctions.indexOf('folds') > -1 || optionInfo.priceFunctions.indexOf('collectingFolds') > -1;
            };
    
            $scope.saveMultiCalculation = function (amount, volume) {
                var preparedProduct = getPreparedProduct(amount, volume);
    
                preparedProduct.isMultiVolumeOffer = 1;
                preparedProduct.multiOfferProductID = currentProductID;
    
                preparedProduct.price = $scope.sellerForm.price;
                preparedProduct.name = $scope.productItem.name;
                preparedProduct.files = $scope.sellerForm.files;
                preparedProduct.updateReason = $scope.sellerForm.updateReason;
    
                if (typeOfResource.type === 'offer') {
                    preparedProduct.isOffer = 1;
                }
    
                console.log('orderID '+orderID);
                preparedProduct.isSeller = 1;
                if (orderID) {
                    preparedProduct.orderID = orderID;
                }
                if (currentProductID) {
                    preparedProduct.productID = currentProductID;
                }
                if ($scope.currentCalc) {
                    preparedProduct.baseID = $scope.currentCalc.baseID;
                }
    
                if ($state.params.customProductID) {
                    preparedProduct.customProductID = $state.params.customProductID;
                }
    
                CalculateService = new PsCalculateService(preparedProduct.groupID, preparedProduct.typeID);
                CalculateService.saveCalculation(preparedProduct).then(function (data) {
                    Notification.success($filter('translate')('success'));
                    var userID = $scope.currentUser ? $scope.currentUser.ID : null;
    
                    orderID = data.orderID;
                    currentProductID = data.productID;
                    $scope.currentProductID = currentProductID;
                    $scope.currentMultiOfferVolumes = data.currentMultiOfferVolumes;
    
                }, function (data) {
                    Notification.error($filter('translate')('error'));
                });
            };
    
            $scope.leaveCalc = function (data) {
                if(data){
                if (typeOfResource.type === 'order') {
    
                    if ($scope.currentCalc) {
                        $state.go('order-list');
                    } else {
                        $state.go('unfinished-orders', {'orderID': data.orderID, 'userID': userID});
                    }
    
                } else {
                        $state.go('unfinished-offers', {'orderID': data.orderID, 'userID': userID});
                }
            }else{
                $state.go('unfinished-offers', {'orderID': orderID, 'userID': userID});
            }
            };
    
            $scope.deleteMultiOffer = function (offer) {
                var CalculateService = new PsCalculateService(0,0);
                CalculateService.deleteMultiOffer({productID: currentProductID, ID: offer.ID}).then(function (data) {
                    $scope.currentMultiOfferVolumes = data.currentMultiOfferVolumes;
                    Notification.success($filter('translate')('success'));
                });
            };
    
            $scope.edit = function (calcID) {
                var params = {
                    'orderID': orderID,
                    'groupID': $scope.group.ID,
                    'typeID': $scope.type.ID,
                    'calcID': calcID,
                    'productID': currentProductID
                };
                $state.go('create-offer-calc', params);
            };
    
            $scope.changeRealizationTime = function (productItem) {
                $scope.showVolumes(_.findWhere($scope.realisationTimes, {ID: productItem.realisationTime}));
            };
    
            $scope.switchDescription = function ($event, data) {
                if ($event.target.innerHTML.length) {
                    $event.target.innerHTML = '';
                } else {
                   data.split('|').forEach(function(text) {
                       var p = document.createElement('p');
                       p.innerHTML = text;
                       $event.target.appendChild(p);
                   });
                }
            };
    
            $scope.initCollapse=function(workspace,printType,info){
                workspace.collapse = !(workspace.workspaceID === info.selectedPrintType.workspaceID && printType.printTypeID === info.selectedPrintType.printTypeID);
            };
            init();
    
        });
