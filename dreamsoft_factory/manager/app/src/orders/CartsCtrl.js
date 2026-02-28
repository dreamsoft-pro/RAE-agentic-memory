angular.module('digitalprint.app')
  .controller('orders.CartsCtrl', function($config, $scope, $state, $filter, $modal, $timeout, ApiCollection, CartService, StatusService, Notification){

    // $scope.opened = false;
    // $scope.openDate = function($event) {
    //   $event.preventDefault();
    //   $event.stopPropagation();
    //   $scope.opened = !$scope.opened;
    // }
    // $scope.$watch('opened', function(newVal) {
    //   console.log(newVal);
    // })

    $scope.showRows = 25;

    $scope.cartsConfig = {
      count: 'carts/count',
      params: {
        limit: $scope.showRows
      },
      onSuccess: function(data){
        $scope.cartsCtrl.items = data;
        setTimeout(function() {
          $('.div1').width( $('.overflowContainer > table').outerWidth());
        }, 300);

      }
    };

    if($state.params.cartID) {
      $scope.cartsConfig.params.ID = $state.params.cartID;
    }

    $scope.cartsCtrl = new ApiCollection('carts', $scope.cartsConfig);
    $scope.cartsCtrl.get();

    var updateTableTimeout;
    $scope.setParams = function() {
      console.log('zmiana parametrów');
      $timeout.cancel(updateTableTimeout);

      updateTableTimeout = $timeout(function(){
        $scope.cartsCtrl.get();
      }, 1000);
    };


    StatusService.getAll().then(function(data) {
      $scope.statuses = data;
    });

    $scope.invoiceData = function(cart) {
      $modal.open({
        templateUrl: 'src/orders/templates/modalboxes/invoice-data.html',
        controller: function($scope) {
          $scope.cart = cart;
        }
      })
    };

    $scope.getAttachment = function(attachment) {
      return $config.API_URL + attachment;
    };

    $scope.toggleValue = function(item, prop){

      var data = {};
      data[prop] = !!! item[prop];

      CartService.patch(item.ID, data).then(function(res){
        item[prop] = data[prop];
      });
    };

    $scope.showMessages = function(cart) {
      $modal.open({
        templateUrl: 'src/orders/templates/modalboxes/cart-messages.html',
        scope: $scope,
        controller: function() {
          $scope.cart = cart;
          $scope.currentMessages = [];

          CartService.messages(cart.ID).then(function(data) {
            $scope.currentMessages = data;
          }, function(data) {
            Notification.error($filter('translate')('error'));
          });

          $scope.send = function(content) {
            CartService.addMessage(cart.ID, content).then(function(data) {
              $scope.content = {};
              $scope.currentMessages.push(data);
              Notification.success($filter('translate')('success'));
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });
          }
          
        }
      })
    };

    $scope.changeStatus = function(cart) {
      console.log(cart);
      CartService.patch(cart.ID, {status: cart.status}).then(function(data) {
        Notification.success($filter('translate')('success'));

      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    };

    $scope.export = function() {

      CartService.export($scope.cartsCtrl.params).then(function(data) {
        Notification.success("Eksport pomyślny");
        $modal.open({
          templateUrl: 'src/orders/templates/modalboxes/carts-export.html',
          scope: $scope,
          controller: function($scope, $modalInstance) {
            $scope.apiUrl = data.apiUrl;
            $scope.exportPath = data.path;
          }
        });

      }, function(data) {
        Notification.error("Error");
      });
    }

  });