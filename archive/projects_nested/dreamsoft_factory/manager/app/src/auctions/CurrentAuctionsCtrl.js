angular.module('digitalprint.app')
    .controller('auctions.CurrentAuctionsCtrl', function ($scope, $filter, $modal, $q, $timeout, OfferService,
                                                          AuctionService, Notification) {

        function init() {

            OfferService.getCompanies().then(function (data) {
                $scope.companies = data;
            }, function (data) {
                Notification.error($filter('translate')('data_retrieve_failed'));
            });

            $scope.filter = {};
            $scope.action = 'open';
            $scope.show($scope.action);
        }

        $scope.selectWinner = function (auction) {
            $modal.open({
                templateUrl: 'src/auctions/templates/modalboxes/accept-auction.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.auction = auction;
                    $scope.form = {};
                    $scope.responses = [];
                    var selectWinnerModalInstance = $modalInstance;

                    AuctionService.allresponses(auction.ID).then(function (data) {
                        $scope.responses = data;
                        console.log($scope.responses);
                    }, function (data) {
                        Notification.error($filter('translate')('data_retrieve_failed'));
                    });

                    $scope.makeAnswer = function (response) {
                        $modal.open({
                            templateUrl: 'src/auctions/templates/modalboxes/make-answer.html',
                            scope: $scope,
                            size: 'lg',
                            controller: function ($scope, $modalInstance) {
                                $scope.response = response;
                                $scope.form = _.clone(response, true);
                                console.log($scope.response);

                                $scope.saveWinner = function () {
                                    delete $scope.form.realizationDate;
                                    $q.all([
                                        AuctionService.editResponse(auction.ID, $scope.form),
                                        AuctionService.selectWinner(auction.ID, response.ID)
                                    ]).then(function (data) {
                                        console.log(data);
                                        var idx = _.findIndex($scope.auctions, {ID: auction.ID});
                                        if (idx > -1) {
                                            $scope.auctions.splice(idx, 1);
                                        }
                                        Notification.success($filter('translate')('success'));
                                        $modalInstance.close();
                                        selectWinnerModalInstance.close();
                                    }, function (data) {
                                        Notification.error($filter('translate')('error'));
                                    });
                                }
                            }
                        });
                    }

                }
            })
        };

        $scope.getCompany = function (companyID) {
            return _.findWhere($scope.companies, {companyID: companyID});
        };

        $scope.show = function (action) {
            $scope.filter = {};

            var now = new Date();
            $scope.auctions = [];
            $scope.action = action;
            if (action == 'open') {
                $scope.filter.open = '1';
            } else if (action == 'close') {
                $scope.filter.close = '1';
                $scope.filter.inRealization = 0;
            } else if (action == 'send') {
                $scope.filter.inRealization = 1;
            } else if (action == 'inOrder') {
                $scope.filter.close = '1';
                $scope.filter.inOrder = 1;
                $scope.filter.inRealization = 1;
            }
            $scope.getAuctions();
        };

        $scope.getFile = function (file) {
            return OfferService.getFile(file.ID);
        };

        $scope.getAuctionFile = function (auction, file) {
            return AuctionService.getFile(auction.ID, file.ID);
        };

        $scope.getAuctions = function () {
            AuctionService.getAuctions($scope.filter).then(function (data) {
                $scope.auctions = data;
                console.log(data);
            });
        };

        $scope.showWinner = function (auction) {
            $modal.open({
                templateUrl: 'src/auctions/templates/modalboxes/show-winner.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.auction = auction;

                    AuctionService.responseWinner(auction.ID).then(function (data) {
                        $scope.response = data;
                    }, function (data) {
                        Notification.error($filter('translate')('error'));
                    });
                }
            });
        };

        $scope.showCurrentOffers = function (auction) {
            $modal.open({
                templateUrl: 'src/auctions/templates/modalboxes/show-current-offers.html',
                scope: $scope,
                size: 'lg',
                controller: function ($scope, $modalInstance) {
                    $scope.responses = [];
                    $scope.auction = auction;

                    AuctionService.allresponses(auction.ID).then(function (data) {
                        $scope.responses = data;
                    }, function (data) {
                        Notification.error($filter('translate')('data_retrieve_failed'));
                    });

                }
            });
        };

        $scope.finishAuction = function (auction) {
            AuctionService.finishAuction(auction.ID).then(function (data) {
                var idx = _.findIndex($scope.auctions, {ID: auction.ID});
                if (idx > -1) {
                    $scope.auctions.splice(idx, 1);
                }
            });
        };

        var updateTableTimeout;
        $scope.setParams = function () {
            console.log('zmiana parametrów');
            $timeout.cancel(updateTableTimeout);

            updateTableTimeout = $timeout(function () {
                $scope.getAuctions();
            }, 1000);
        };

        $scope.setDate = function () {
            console.log($scope.filter);
            if (angular.isDefined($scope.filter.createdFrom) || angular.isDefined($scope.filter.createdTo)) {
                $scope.getAuctions();
            }
        };

        $scope.export = function () {
            AuctionService.export($scope.filter).then(function (data) {
                Notification.success("Eksport pomyślny");
                $modal.open({
                    templateUrl: 'src/auctions/templates/modalboxes/auctions-export.html',
                    scope: $scope,
                    controller: function ($scope, $modalInstance) {
                        $scope.apiUrl = data.apiUrl;
                        $scope.exportPath = data.path;
                    }
                });
                console.log(data);
            }, function (data) {
                Notification.error("Error");
            });
        };

        init();

    });