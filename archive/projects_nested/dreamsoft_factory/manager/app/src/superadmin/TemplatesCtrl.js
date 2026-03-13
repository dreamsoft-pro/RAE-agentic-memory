angular.module('digitalprint.app')
  .controller('superadmin.TemplatesCtrl', function($scope, $filter, $modal, Notification, TemplateRootService) {

   function readList(){
     TemplateRootService.getAll().then(function(data) {
       $scope.templates = data;
     });
   }
    readList();
    $scope.add = function() {

      TemplateRootService.add($scope.form).then(function(data) {
        readList();
        $scope.form = {};
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));
      });
    };

    $scope.remove = function(template) {

      TemplateRootService.remove(template.ID).then(function(data) {

        readList();
        Notification.success($filter('translate')('success'));

      }, function(data) {

        Notification.error($filter('translate')('error') + ' ' + (data.info || data.error || ''));

      });
    };

    $scope.edit = function(template) {
      $modal.open({
        templateUrl: 'src/superadmin/templates/modalboxes/edit-template.html',
        scope: $scope,

        controller: function($scope, $modalInstance) {
          $scope.template = _.clone(template);
          $scope.form = _.clone(template);

          $scope.ok = function() {
            TemplateRootService.edit($scope.form).then(function(data) {
              $modalInstance.close();
              Notification.success($filter('translate')('success'));
              readList();
            }, function(data) {
              Notification.error($filter('translate')('error') + ' ' + data.info)
            });
          }
        }
      });

    };

  });
