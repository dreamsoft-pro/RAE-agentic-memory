angular.module('digitalprint.app')
  .controller('customerservice.CalculationsListCtrl', function($scope, $state, $filter, $modal, CalculationService, UserService, Notification){

    CalculationService.getAllSeller().then(function(data) {
      $scope.calculations = data;
    }, function(data) {
      Notification.error($filter('translate')('data_retrieve_failed'));
    });

    // $scope.showRows = 25;

    $scope.edit = function(calculation) {
      console.log(calculation);
      var params = {
        'groupID': calculation.groupID,
        'typeID': calculation.typeID,
        'calcID': calculation.ID
      };
      $state.go('create-order-calc', params);
    }

    $scope.history = function(calculation) {
      $modal.open({
        templateUrl: 'src/customerservice/templates/modalboxes/calculation-history.html',
        scope: $scope,
        size: 'lg',
        resolve: {
          calculations: function(CalculationService) {
            return CalculationService.history(calculation.baseID).then(function(data) {
              return data;
            }, function(data) {
              console.error(data);
              Notification.error($filter('translate')('data_retrieve_failed'));
            });
          }
        },
        controller: function($scope, $modalInstance, calculations) {
          $scope.calculations = calculations;
          $scope.edit = function(calculation) {
            $scope.$parent.edit(calculation);
            $modalInstance.close();
          }
          $scope.makeOrder = function(calculation) {
            $scope.$parent.makeOrder(calculation);
            $modalInstance.close();
          }
        }
      });
    }

    $scope.makeOrder = function(calculation) {
    }

  });