angular.module('digitalprint.app')
  .controller('orders.AuctionsListCtrl', function($scope, $filter, $modal, AuctionService, OfferService, Notification) {

    // AuctionService.forCompany().then(function(data) {
    //   $scope.auctions = data;
    // }, function(data) {
    //   Notification.error($filter('translate')('data_retrieve_failed'));
    // });
    function init() {
      $scope.filter = {};
      $scope.action = 'open';
      $scope.show($scope.action);
    }

    $scope.answerAuction = function(auction) {
      $modal.open({
        templateUrl: 'src/orders/templates/modalboxes/answer-auction.html',
        scope: $scope,
        size: 'lg',
        controller: function($scope, $modalInstance) {
          $scope.form = {};
          $scope.auction = auction;

          $scope.form.realizationDate  = new Date($scope.auction.realizationDate);
          console.log($scope.form.realizationDate);

          AuctionService.response(auction.ID).then(function(data) {
            $scope.responses = data;
            // if(!_.isArray(data)) {
            //   $scope.form = data;
            //   // var date = Math.floor(new Date($scope.form.realizationDate).valueOf()/1000);
            //   $scope.form.realizationDate = new Date($scope.form.realizationDate);
            // } else {
            // }
          }, function(data) {
            Notification.error($filter('translate')('error'));
          });

          $scope.answer = function() {
            // $scope.form.companyID = $scope.currentDomain.companyID;
            AuctionService.addResponse(auction.ID, $scope.form).then(function(data) {
              console.log(data);
              Notification.success($filter('translate')('success'));
              $scope.responses.push(data.item);
              auction.hasResponse = 1;
              $scope.form = {};
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });
          }

          $scope.editAnswer = function(response) {
            $modal.open({
              templateUrl: 'src/orders/templates/modalboxes/edit-answer-auction.html',
              scope: $scope,
              controller: function($scope, $modalInstance) {
                $scope.form = _.clone(response, true);
                $scope.form.realizationDate = new Date($scope.form.realizationDate);
                // $scope.form.realizationDate = realizationDate.valueOf()/1000;

                $scope.save = function() {
                  AuctionService.editResponse(auction.ID, $scope.form).then(function(data) {
                    Notification.success($filter('translate')('success'));
                    var idx = _.findIndex($scope.responses, {ID: data.item.ID});
                    if(idx > -1) {
                      $scope.responses[idx] = data.item;
                    }
                    $modalInstance.close();
                  }, function(data) {
                    Notification.error($filter('translate')('error'));
                  });
                }
              }
            });
            
          }
        }
      });
    }

    $scope.showAuctionAnswer = function(auction) {
      $modal.open({
        templateUrl: 'src/orders/templates/modalboxes/show-answer-auction.html',
        scope: $scope,
        size: 'lg',
        controller: function($scope, $modalInstance) {
          $scope.auction = auction;
          AuctionService.response(auction.ID).then(function(data) {
            $scope.responses = data;
          }, function(data) {
            Notification.error($filter('translate')('error'));
          });
        }
      });
    }

    $scope.show = function(action) {
      $scope.filter = {};
      // nie wiem czy dobrze biorę czas
      var now = new Date();
      $scope.auctions = [];
      $scope.action = action;
      if(action == 'open') {
        // $scope.filter.endDateMax = Math.floor(now.valueOf()/1000);
        $scope.filter.open = '1';
      } else if(action == 'close') {
        // $scope.filter.endDateMin = Math.floor(now.valueOf()/1000);
        $scope.filter.close = '1';
        $scope.filter.inRealization = 0;
      } else if(action == 'send') {
        // $scope.filter.endDateMin = Math.floor(now.valueOf()/1000);
        // $scope.filter.close = '1';
        $scope.filter.inRealization = 1;
      } else if(action == 'inOrder') {
        // $scope.filter.endDateMin = Math.floor(now.valueOf()/1000);
        $scope.filter.close = '1';
        $scope.filter.inOrder = 1;
        $scope.filter.inRealization = 1;
      }
      $scope.getAuctions();
    }

    $scope.getAuctions = function() {
      AuctionService.forCompany($scope.filter).then(function(data) {
        $scope.auctions = data;
        console.log(data);
      }, function(data) {
        Notification.error($filter('translate')('data_retrieve_failed'));
      });
    }

    $scope.getFile = function(file, fromCompanyID) {
      //console.log( fromCompanyID );
      return OfferService.getFile(file.ID, fromCompanyID);
    };

    $scope.getAuctionFile = function(auction, file) {
      return AuctionService.getFile(auction.ID, file.ID);
    }

    // $scope.showRows = 25;
    // $scope.ordersConfig = {
    //   count: 'orders/count',
    //   params: {
    //     limit: $scope.showRows,
    //     accept: 0
    //   },
    //   onSuccess: function(data){
    //     $scope.ordersCtrl.items = data;
    //   }
    // }

    // $scope.ordersCtrl = new ApiCollection('orders', $scope.ordersConfig);
    // $scope.ordersCtrl.get();

    // var updateTableTimeout;

    // $scope.setParams = function() {
    //   $timeout.cancel(updateTableTimeout);
    //   updateTableTimeout = $timeout(function(){
    //     $scope.ordersCtrl.get();
    //   }, 1000);
    // }

    // $scope.accept = function(order, accept) {
    //   var accept = accept ? 1 : -1;

    //   OrderService.accept(order.ID, accept).then(function(data) {
    //     var idx = _.findIndex($scope.ordersCtrl.items, {ID: order.ID});
    //     if(idx > -1) {
    //       $scope.ordersCtrl.items.splice(idx, 1);
    //     }
    //     Notification.success($filter('translate')('success'));
    //   }, function(data) {
    //     Notification.error($filter('translate')('error'));
    //   })
    // }
    init();

  });