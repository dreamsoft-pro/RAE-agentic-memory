angular.module('digitalprint.app')
  .controller('contents.TypeDescriptionsCtrl', function($scope, $filter, $modal, TypeDescriptionsService, Notification){
  	  	$scope.descriptionsForm = {};

     TypeDescriptionsService.create($scope.descriptionForm).then(function(data) {
        if( data.item.parentID > 0 ){
          var idx = _.findIndex($scope.name, {ID: data.item.parentID});
        } else {
          $scope.categories.push(data.item);
        }
        
        $scope.categoryForm = {};
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });

    }


);
