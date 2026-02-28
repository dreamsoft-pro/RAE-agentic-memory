angular.module('digitalprint.app')
    .controller('customerservice.OfferListCtrl', function ($scope, $filter, $modal, OfferService, AuctionService,
                                                           Notification) {

        function getOffers() {
            OfferService.getAll({finished: 1}).then(function (data) {
                $scope.offers = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

        }

        getOffers();

        $scope.showWinner = function (offer) {
            $modal.open({
                templateUrl: 'src/customerservice/templates/modalboxes/show-winner.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.offer = offer;
                    $scope.form = {};

                    AuctionService.responseWinner(offer.auctionInfo.ID).then(function (data) {
                        $scope.response = data;
                    }, function (data) {
                        Notification.error($filter('translate')('error'));
                    });

                    $scope.makeOrder = function () {
                        var products = [];
                        _.each(offer.items, function (item) {
                            if (item.selected) {
                                products.push(item.ID);
                            }
                        });
                        if (!products.length) {
                            Notification.error('Wybierz co najmniej jeden produkt');
                            return true;
                        }

                        console.log(products);
                        var data = {
                            products: products,
                            orderDescription: $scope.form.orderDescription,
                            poNumber: $scope.form.poNumber
                        };
                        var auctionID = offer.auctionInfo.ID;
                        AuctionService.order(auctionID, data).then(function (data) {
                            $modalInstance.close();
                            getOffers();
                            Notification.success($filter('translate')('success'));
                        }, function (data) {
                            Notification.error($filter('translate')('error'));
                        });
                    }
                }
            });
        };

        $scope.getFile = function (file) {
            return OfferService.getFile(file.ID);
        };

        $scope.getAuctionFile = function (offer, file) {
            return AuctionService.getFile(offer.auctionInfo.ID, file.ID);
        };

        $scope.uploadAuctionFile = function (offer) {
            console.log('upload');

            if (offer.files && offer.files.length) {
                _.each(offer.files, function (file) {
                    AuctionService.uploadFile(offer.auctionInfo.ID, file).progress(function (evt) {
                        offer.progress = parseInt(100.0 * evt.loaded / evt.total);
                    }).success(function (data, status, headers, config) {
                        offer.progress = 0;
                        offer.fileList.push(data.file);
                        Notification.success($filter('translate')('success'));
                    }).error(function (data, status, headers, config) {
                        console.log('error status' + status);
                        Notification.error($filter('translate')('error' + status));
                    });
                });
            }
        };

        $scope.removeAuctionFile = function (offer, file) {
            AuctionService.removeFile(offer.auctionInfo.ID, file.ID).then(function (data) {

                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error' + status));
            });
        };

        $scope.getAuctionFile = function (offer, file) {
            return AuctionService.getFile(offer.auctionInfo.ID, file.ID);
        }

    });