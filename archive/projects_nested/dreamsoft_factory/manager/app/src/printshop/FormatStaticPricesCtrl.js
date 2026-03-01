'use strict';

angular.module('digitalprint.app')
    .controller('printshop.FormatStaticPricesCtrl', function ($rootScope, $scope, $stateParams, $filter, Notification,
                                                              $modal, PsFormatService, PsPrintTypeService, getData,
                                                              PsPageService, $q, PsAttributeService, PsVolumeService,
                                                              $document, PsStaticPrice, FileUploader, $config,
                                                              Pagination) {
        var currentGroupID;
        var currentTypeID;
        var currentFormatID;

        var multipleSort = false;
        $scope.sortArray = [];
        $document.keydown(function (e) {
            if (e.keyCode === 17) {
                multipleSort = true;
            }
        });
        $document.keyup(function (e) {
            if (e.keyCode === 17) {
                multipleSort = false;
            }
        });

        $scope.paginationSettings = {
            currentPage: 0,
            pageSize: 25,
            numberOfPages: 1,
            maxSize: 21,
            sortingReverse: false,
            sortingOrder: ''
        };

        $scope.paginationAPI = Pagination;

        $scope.formats = [];
        currentGroupID = $scope.currentGroupID = $stateParams.groupID;
        currentTypeID = $scope.currentTypeID = $stateParams.typeID;
        currentFormatID = $scope.currentFormatID = $stateParams.formatID;

        $rootScope.currentTypeName = getData.type.name;
        $rootScope.currentGroupName = getData.group.name;

        var FormatService = new PsFormatService(currentGroupID, currentTypeID);

        FormatService.getAll().then(function (data) {
            $scope.formats = data;
            $scope.currentFormat = _.findWhere($scope.formats, {ID: currentFormatID});
        }, function (data) {
            Notification.error($filter('translate')('error'));
        });

        $scope.pages = [];

        var PageService = new PsPageService(currentGroupID, currentTypeID);

        var pages = PageService.getAll().then(function (data) {
            if (!data.length) {
                $scope.pages = [{pages: 2}];
                return true;
            }
            if (_.first(data).minPages) {
                $scope.rangePages = true;
                return $q.reject({rangePages: true});
            } else {
                $scope.pages = data;
            }
        });


        var AttributeService = new PsAttributeService(currentGroupID, currentTypeID);
        var VolumeService = new PsVolumeService(currentGroupID, currentTypeID);
        var StaticPriceService = new PsStaticPrice(currentGroupID, currentTypeID, currentFormatID);


        pages.then(function (data) {
            $q.all([
                AttributeService.getAll(),
                VolumeService.getAll(),
                StaticPriceService.getAll()
            ]).then(function (data) {
                $scope.selectedOptions = data[0];
                groupOptions($scope.selectedOptions);
                $scope.volumes = data[1];
                //$scope.staticPrices = data[2];
                staticPriceMatrix().then(function() {
                    staticPricesSuccess(data[2]);
                });
            });
        }, function (data) {

        });

        $scope.sortBy = function (orderBy) {
            if (!($scope.sortArray.length === 1 && _.contains($scope.sortArray, orderBy))) {

                if (!multipleSort) {
                    $scope.sortArray = [];
                }
            }
            if (_.contains($scope.sortArray, orderBy)) {
                $scope.sortArray = _.without($scope.sortArray, orderBy);
                $scope.sortArray.push('-' + orderBy);
            } else if (_.contains($scope.sortArray, '-' + orderBy)) {
                $scope.sortArray = _.without($scope.sortArray, '-' + orderBy);
                $scope.sortArray.push(orderBy);
            } else {
                $scope.sortArray.push(orderBy);
            }

            $scope.filteredMatrix = $filter('orderBy')($scope.matrix, $scope.sortArray);

        };

        $scope.getPriceKey = function (price) {
            var pureObj = {};

            for (var key in price) {
                if (price.hasOwnProperty(key) && key != '$$hashKey') {
                    pureObj[key] = price[key];
                }
            }
            return JSON.stringify(pureObj);
        };

        $scope.savePrice = function (price) {
            var item = {price: price.price, options: price.options};
            StaticPriceService.set(item).then(function (data) {
                Notification.success("Ok");
            }, function (data) {
                Notification.error("Error");
            });
        };

        $scope.saveExpense = function (price) {
            var item = {expense: price.expense, options: price.options};
            StaticPriceService.set(item).then(function (data) {
                Notification.success("Ok");
            }, function (data) {
                Notification.error("Error");
            });
        };

        $scope.export = function () {
            StaticPriceService.export().then(function (data) {
                Notification.success("Eksport pomyślny");
                $modal.open({
                    templateUrl: 'src/printshop/templates/modalboxes/static-prices-export.html',
                    scope: $scope,
                    controller: function ($scope, $modalInstance) {
                        $scope.exportPaths = data.urls;
                    }
                });
            }, function (data) {
                Notification.error("Error");
            });
        };

        $scope.importDialog = function () {
            $modal.open({
                templateUrl: 'src/printshop/templates/modalboxes/static-prices-import.html',
                scope: $scope,
                controller: function ($scope, $modalInstance) {
                    $scope.uploader = new FileUploader({
                        url: $config.API_URL + [StaticPriceService.resource, 'import'].join('/'),
                        autoUpload: true,
                        queueLimit: 1
                    });

                    $scope.uploader.onSuccessItem = function (item, data) {
                        if (data.response) {
                            Notification.success('Import pomyślny');
                            StaticPriceService.getAll(true).then(function (data) {
                                $scope.staticPrices = data;
                                staticPricesSuccess(data);
                                Notification.success('Ceny odświeżone');
                            });
                        } else {
                            Notification.error("Error");
                        }
                    }

                }
            })
        };

        var groupOptions = function (data) {
            var selectedOptions = data;
            $scope.groupOptions = {};

            _.each(selectedOptions, function (value, key) {

                if ($scope.groupOptions[value.attrID] === undefined) {
                    $scope.groupOptions[value.attrID] = {};
                }
                if ($scope.groupOptions[value.attrID][value.optID] === undefined) {
                    $scope.groupOptions[value.attrID][value.optID] = {};
                }

                $scope.groupOptions[value.attrID][value.optID] = value;

            });

        };

        var staticPriceMatrix = function () {

            var def = $q.defer();

            var matrix = [];

            addPagesToMatrix($scope, matrix).then(function (matrix) {
                addVolumesToMatrix($scope, matrix).then(function (matrix) {
                    addOptionsToMatrix($scope, matrix).then(function (matrix) {

                        $scope.matrix = matrix;

                        _.each($scope.matrix, function (item, actualIndex) {
                            item.options = $scope.getPriceKey(item);

                            if (actualIndex === ($scope.matrix.length - 1)) {
                                def.resolve(true);
                            }
                        });

                        $scope.filteredMatrix = $scope.matrix;
                        $scope.paginationSettings.numberOfPages = Math.ceil($scope.filteredMatrix.length / $scope.paginationSettings.pageSize);


                    });
                });
            });

            return def.promise;

        };

        var staticPricesSuccess = function (staticPrices) {
            _.each(staticPrices, function (item) {
                var options = JSON.parse(item.options);
                item.json = options;
                item.options = JSON.stringify(item.json);
            });

            _.each($scope.matrix, function (item) {
                var price = _.findWhere(staticPrices, {options: item.options});
                if (price !== undefined) {
                    item.price = price.price;
                    item.expense = price.expense || '';
                } else {
                    item.price = '';
                    item.expense = '';
                }
            });

        };

        function addPagesToMatrix(scope, matrix) {
            var def = $q.defer();

            for (var pagesIndex = 0, len = scope.pages.length; pagesIndex < len; pagesIndex++) {
                matrix.push({'pages': scope.pages[pagesIndex].pages});
                if (pagesIndex === (scope.pages.length - 1)) {
                    def.resolve(matrix);
                }
            }

            return def.promise;
        }

        function addOptionsToMatrix(scope, matrix) {

            var def = $q.defer();

            var sizeOfAttributes = _.size(scope.groupOptions);
            var counterAttributes = 0;
            var counterOptions = 0;
            var counterMatrix = 0;

            for (var attrID in scope.groupOptions) {

                var newMatrix = _.clone(matrix, true);
                var sizeOfNewMatrix = _.size(newMatrix);

                matrix = [];

                var sizeOfOptions = _.size(scope.groupOptions[attrID]);
                counterOptions = 0;

                for (var optID in scope.groupOptions[attrID]) {

                    counterMatrix = 0;

                    for (var index in newMatrix) {

                        var tmp = {};
                        for (var item in newMatrix[index]) {
                            if (newMatrix[index].hasOwnProperty(item)) {
                                tmp[item] = newMatrix[index][item];
                            }
                        }
                        tmp[attrID] = parseInt(optID);
                        matrix.push(tmp);
                        if (counterAttributes === (sizeOfAttributes - 1) &&
                            counterOptions === (sizeOfOptions - 1) &&
                            counterMatrix === (sizeOfNewMatrix - 1)) {
                            def.resolve(matrix);
                        }

                        counterMatrix++;
                    }
                    counterOptions++;
                }

                counterAttributes++;
            }

            return def.promise;

        }

        function addVolumesToMatrix(scope, matrix) {

            var def = $q.defer();

            var newMatrix = _.clone(matrix, true);
            matrix = [];

            var sizeOfVolumes = _.size(scope.volumes);
            var sizeOfNewMatrix = _.size(newMatrix);
            var volumesCounter = 0;
            var counterMatrix = 0;

            for (var volumeIndex in scope.volumes) {

                if (scope.volumes[volumeIndex].length) {
                    if (_.indexOf(scope.volumes[volumeIndex].formats, parseInt(currentFormatID)) === -1) {
                        return true;
                    }
                }

                counterMatrix = 0;

                for (var indexMatrix in newMatrix) {
                    var tmp = {};
                    for (var item in newMatrix[indexMatrix]) {
                        if (newMatrix[indexMatrix].hasOwnProperty(item)) {
                            tmp[item] = newMatrix[indexMatrix][item];
                        }
                    }
                    tmp['volumes'] = scope.volumes[volumeIndex].volume;
                    matrix.push(tmp);

                    if (volumesCounter === (sizeOfVolumes - 1) &&
                        counterMatrix === (sizeOfNewMatrix - 1)) {
                        def.resolve(matrix);
                    }
                    counterMatrix++;
                }

                volumesCounter++;
            }

            return def.promise;

        }

    });