angular.module('digitalprint.app')
  .controller('auctions.OfferListCtrl', function($scope, $filter, $modal, OfferService, AuctionService, Notification){

      OfferService.getAll({finished: 1, auction: 0}).then(function(data) {
        $scope.offers = data;
      }, function(data) {
        Notification.error($filter('translate')('data_retrieve_failed'));
      });
      

    $scope.refresh = function() {
      OfferService.getAll({finished: 1, auction:0});
    }

    OfferService.getCompanies().then(function(data) {
      $scope.companies = data;
    }, function(data) {
      Notification.error($filter('translate')('data_retrieve_failed'));
    });

    $scope.createAuction = function(offer) {

      $modal.open({
        templateUrl: 'src/auctions/templates/modalboxes/create-auction.html',
        scope: $scope,
        size: 'lg',
        controller: function($scope, $modalInstance) {
          $scope.form = {};

          $scope.form.time = new Date(43200000); // ustawiam zegarek na 12
          $scope.currentOffer = offer;
          _.each($scope.companies, function(item) {
            item.selected = false;
          })
          $scope.selectCompany = function(company) {
            company.selected = !company.selected;
          }
          $scope.makeAuction = function(form) {
            // console.log(form.time.valueOf()/1000);
            var time = form.time.valueOf()/1000;

            console.log('time', time);
            time+= 3600; // coś jest nie tak (strefa czasowa)
            // return false;
            var item = {};
            item.offerID = offer.ID;
            item.endDate = form.endDate+time;
            item.description = form.description;
            item.companies = [];
            _.each($scope.companies, function(each) {
              if(each.selected) {
                item.companies.push(each.companyID);
              }
            });
            //endDate
            //offerID
            //companies = [];
            //description
            console.log(item);
            AuctionService.create(item).then(function(data) {
              // TODO delete auction from actions
              var idx = _.findIndex($scope.offers, {ID: offer.ID});
              if(idx > -1) {
                $scope.offers.splice(idx, 1);
              }
              Notification.success($filter('translate')('success'));
              $modalInstance.close();
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });
          }
          $scope.changed = function(time) {
            console.log(time)
          }
        }
      })
    }

    $scope.getFile = function(file) {
      return OfferService.getFile(file.ID);
    }

    $scope.userCanAddFile = function() {
      //console.log('--------------------------TU>>>>>>>>>>>>>>>>');
      OfferService.userCanAddFile().then(function(data) {
        if( data.response == true ){
          return true;
        }
      }, function(data) {
        return false;
        //Notification.error($filter('translate')('data_retrieve_failed'));
      });
    }

    $scope.uploadItemFile = function(item) {

      if(item.uploadFiles && item.uploadFiles.length) {
        _.each(item.uploadFiles, function(file) {
          console.log('item');
          console.log(file);
          OfferService.uploadItemFile(item.ID ,file).progress(function(evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            // console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
            item.progress = progressPercentage;
          }).success(function(data, status, headers, config) {
            // console.log('file ' + config.file.name + 'uploaded. Response: ' + data);
            // console.log(data);
            item.progress = 0;
            if( !item.files ){
              item.files = [];
            }

            item.files.push(data.file);
            Notification.success($filter('translate')('success'));
          }).error(function(data,status, headers, config) {
            console.log('error status' + status);
            Notification.error($filter('translate')('error' + status));
          });
        });
      }
    }

    $scope.removeItemFile = function(item, file) {
      OfferService.removeItemFile(file.ID).then(function(data) {
        var idx = _.findIndex(item.files, {ID: file.ID});
        if(idx > -1) {
          item.files.splice(idx, 1);
        }
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }

    $scope.toggleVisible = function(file, prop) {

      var data = {};
      data[prop] = !!!file[prop];

      OfferService.toggleVisible(file.ID, data).then(function(res) {
        file[prop] = data[prop];
      });
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

  });