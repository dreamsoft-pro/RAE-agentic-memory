angular.module('digitalprint.app')
  .controller('printshop.SkillsCtrl', function($scope, $filter, $modal, SkillService, DeviceService, Notification){

    SkillService.getAll().then(function(data){
      $scope.skills = data;
    });

    $scope.add = function() {
      SkillService.create($scope.form).then(function(data) {
        $scope.skills.push(data);
        $scope.form = {};
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }

    $scope.edit = function(skill){
      $modal.open({
        templateUrl: 'src/printshop/templates/modalboxes/edit-skill.html',
        scope: $scope,
        controller: function($scope, $modalInstance){
          $scope.skill = _.clone(skill);
          $scope.form = _.clone(skill);
          
          $scope.ok = function() {
            SkillService.update($scope.form).then(function(data) {
              skill = _.extend(skill, $scope.form);
              $modalInstance.close();
              Notification.success($filter('translate')('success'));
            });
          }
        }
      });
    }

    $scope.devices = function(skill) {
      $modal.open({
        templateUrl: 'src/printshop/templates/modalboxes/skill-devices.html',
        scope: $scope,
        controller: function($scope, $modalInstance) {
          $scope.skill = _.clone(skill);
          $scope.currentDevices = [];
          DeviceService.getAll().then(function(data) {
            //pobieramy wszystkie
            $scope.currentDevices = _.clone(data, true);
            // wybieramy wybrane urządzenia
            SkillService.devices(skill).then(function(data) {
              _.each(data, function(elem) {
                var idx = _.findIndex($scope.currentDevices, {ID: elem});
                if(idx > -1) {
                  $scope.currentDevices[idx].selected = 1;
                }
              })
            });
          });

          $scope.ok = function() {
            var selectedDevices = [];
            _.each($scope.currentDevices, function(each) {
              if(each.selected === 1) {
                selectedDevices.push(each.ID);
              }
            });

            SkillService.setDevices(skill, selectedDevices).then(function(data) {
              console.log(data);
              $modalInstance.close();
              Notification.success($filter('translate')('success'));
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });
          }
        }
      });
    }

    $scope.remove = function(id) {
      SkillService.remove(id).then(function(data) {
        var idx = _.findIndex($scope.skills, {ID: id});
        $scope.skills.splice(idx, 1);
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'))
      })
    };

    $scope.search = function () {
      var newFilter = {};
      for(var filter in $scope.filterData){
          if($scope.filterData[filter] != ''){
              newFilter[filter] = $scope.filterData[filter];
          }
      }
      $scope.filterData = newFilter;
    };

  });