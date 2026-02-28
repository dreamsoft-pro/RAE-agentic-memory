angular.module('digitalprint.app')
  .controller('superadmin.AdminHelpsCtrl', function($scope, $filter, $modal, AdminHelpService, Notification){

    AdminHelpService.getAll().then(function(data){
      $scope.modules = data;
    });

    $scope.add = function() {
      AdminHelpService.create($scope.form).then(function(data) {
        $scope.modules.push(data);
        $scope.form = {};
        Notification.success("Ok");
      }, function(data) {
        Notification.error("Error - " + data.info);
      });
    }

    $scope.edit = function(module){
      $modal.open({
        templateUrl: 'src/superadmin/templates/modalboxes/edit-help-module.html',
        scope: $scope,
        controller: function($scope, $modalInstance){
          $scope.form = $scope.module = _.clone(module);
          
          $scope.ok = function() {
            AdminHelpService.update($scope.form).then(function(data) {
              module = _.extend(module, $scope.form);
              $modalInstance.close();
              Notification.success("Ok");
            });
          }
        }
      });
    }

    $scope.keys = function(module){
      $modal.open({
        templateUrl: 'src/superadmin/templates/modalboxes/help-module-keys.html',
        scope: $scope,
        size: 'lg',
        controller: function($scope, $modalInstance){
          $scope.form =  {};
          $scope.module = _.clone(module);
          $scope.keys = [];

          AdminHelpService.getKeys(module.module).then(function(data) {
            $scope.keys = data;
          });

          $scope.add = function() {
            AdminHelpService.addKey(module.module, $scope.form).then(function(data) {
              $scope.keys.push(data);
              $scope.form = {};
              Notification.success("Ok");
            }, function(data) { Notification.error("Error - " + data.info) });
          }

          $scope.edit = function(key) {
            $modal.open({
              templateUrl: 'src/superadmin/templates/modalboxes/edit-help-module-key.html',
              scope: $scope,
              size: 'lg',
              controller: function($scope, $modalInstance) {
                $scope.form = _.clone(key);
                $scope.key = _.clone(key);

                $scope.ok = function() {
                  AdminHelpService.editKey(module.module, key).then(function(data) {
                    key = _.extend(key, $scope.form);
                    $modalInstance.close();
                    Notification.success("Ok");
                  }, function(data) {
                    Notification.error("Error");
                  })
                }

              }
            })
          }

          $scope.remove = function(keyID) {
            AdminHelpService.removeKey(module.module, keyID).then(function(data) {
              var idx = _.findIndex($scope.keys, {ID: keyID});
              $scope.keys.splice(idx, 1);
              Notification.success("Ok");
            }, function(data) {
              Notification.error("Error");
            })
          }

          // $scope.ok = function() {
          //   AdminHelpService.update($scope.form).then(function(data) {
          //     module = _.extend(module, $scope.form);
          //     $modalInstance.close();
          //     Notification.success("Ok");
          //   });
          // }
        }
      });
    }

    $scope.remove = function(elem) {
      AdminHelpService.remove(elem.ID).then(function(data) {
        var idx = _.findIndex($scope.modules, {ID: elem.ID});
        $scope.modules.splice(idx, 1);
        Notification.success("Ok");
      }, function(data) {
        Notification.error("Error")
      })
    }

  });