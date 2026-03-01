angular.module('digitalprint.helpers')
.directive('ngConfirmClick', [
  function(){
    return {
      restrict: 'A',
      replace: false,
      link: function (scope, element, attr) {
        
        var clickAction = attr.ngConfirmClick;

        element.bind('click',function (event) {
          scope.open();

          scope.onConfirm = function(){
            scope.$eval(clickAction)
          }
        });
      },
      controller: function($scope, $filter, $modal, $sce, $attrs){
        
        var clickAction = $attrs.ngConfirmClick;
        
        $scope.open = function(){
          $modal.open({
            scope: $scope,
            templateUrl: 'views/modalboxes/confirm.html',
            controller: function($scope, $modalInstance){
              $scope.title = $sce.trustAsHtml($attrs.confirmTitle) || $filter('translate')('confirm');
              $scope.description = $sce.trustAsHtml($filter('translate')($attrs.confirmText)) || $sce.trustAsHtml($filter('translate')('irreversible_remove'));

              $scope.confirm = function(){
                $scope.onConfirm();
                $modalInstance.close();
              }

            }
          });
        }

      }
    };
  }]);