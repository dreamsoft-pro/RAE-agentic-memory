angular.module('digitalprint.app')
    .controller('customerservice.OfferInOrderListCtrl', function ($scope, $filter, $modal, OfferService,
                                                                  AuctionService, Notification) {

        function getOffers() {
            OfferService.getAll({finished: 1, inOrder: 1}).then(function (data) {
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
                        var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                        offer.progress = progressPercentage;
                    }).success(function (data, status, headers, config) {
                        offer.progress = 0;
                        if (!offer.auctionFiles) {
                            offer.auctionFiles = [];
                        }
                        offer.auctionFiles.push(data.file);
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
                var idx = _.findIndex(offer.auctionFiles, {ID: file.ID});
                if (idx > -1) {
                    offer.auctionFiles.splice(idx, 1);
                }
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error' + status));
            });
        }

    });