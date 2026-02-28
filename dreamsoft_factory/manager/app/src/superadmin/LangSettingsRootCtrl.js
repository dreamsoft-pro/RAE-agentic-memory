angular.module('digitalprint.app')
  .controller('superadmin.LangSettingsRootCtrl', function($scope, $q, $modal, LangSettingsRootService, Notification){

    $scope.form = {};

    LangSettingsRootService.getAll().then(function(data){
      $scope.langlist = data;
    });

    $scope.refresh = function() {
      LangSettingsRootService.getAll(true).then(function(data){
        $scope.langlist = data;
      });
    }

    $scope.add = function() {
      console.log($scope.form);
      // $scope.form.active = 1;
      LangSettingsRootService.create($scope.form).then(function(data) {
        $scope.langlist.push(data);
        $scope.form = {};
        Notification.success("Ok");
      }, function(data) {
        console.log(data);
        Notification.error("Error");
      });

    }

    $scope.edit = function(lang){
      $modal.open({
        templateUrl: 'src/superadmin/templates/modalboxes/edit-lang-settings.html',
        scope: $scope,
        controller: function($scope, $modalInstance){
          $scope.form = _.clone(lang);
          
          $scope.ok = function() {
            LangSettingsRootService.update($scope.form).then(function(data) {
              lang = _.extend(lang, $scope.form);
              $scope.form = {};
              $modalInstance.close();
              Notification.success("Ok");
            });
          }
        }
      });
    }


    $scope.remove = function(id){

      var idx = _.findIndex($scope.langlist, {
        ID: id
      });

      LangSettingsRootService.remove(id).then(function(){
        $scope.langlist.splice(idx, 1);
        Notification.success('Success');
      });

    }


  });