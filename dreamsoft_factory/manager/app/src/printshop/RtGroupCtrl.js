angular.module('digitalprint.app')
  .controller('printshop.RtGroupCtrl', function($scope, $filter, $stateParams, $modal, Notification, PsGroupService) {

    var currentGroupID;

    function init() {
      currentGroupID = $scope.groupID = $stateParams.groupID;

      PsGroupService.getRealizationTimes(currentGroupID).then(function(data) {
        $scope.realizationTimes = data;
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });

    }

    init();

    $scope.refreshTimes = function() {
      PsGroupService.getRealizationTimes(currentGroupID, true);
    }

    $scope.add = function() {
      // nie dodajemy rt details
    }

    $scope.editStart = function(elem) {
      $modal.open({
        templateUrl: 'src/printshop/templates/modalboxes/edit-realizationtime-details.html',
        scope: $scope,
        controller: function($scope, $modalInstance) {
          $scope.form = {};
          $scope.oryg = elem;

          $scope.form.pricePercentage = elem.details ? elem.details.pricePercentage : elem.pricePercentage;
          $scope.form.active = elem.details ? elem.details.active : elem.active;
          $scope.form.days = elem.details ? elem.details.days : elem.days;
          $scope.form.realizationID = elem.ID;

          $scope.save = function() {

            PsGroupService.setRealizationTime(currentGroupID, $scope.form).then(function(data) {
              console.log(data);
              var idx = _.findIndex($scope.realizationTimes, {ID: $scope.oryg.ID});
              if(idx > -1) {
                $scope.realizationTimes[idx].details = _.clone($scope.form);
                $scope.realizationTimes[idx].details.ID = data.data.ID;
              }
              Notification.success($filter('translate')('success'));
              $modalInstance.close();
            }, function(data) {
              Notification.error($filter('translate')('error'));
            });

          }

          $scope.cancel = function() {
            $modalInstance.close();
          }

        }
      })
    }

    $scope.remove = function(elem) {

      PsGroupService.removeRealizationTime(currentGroupID, elem).then(function(data) {
        var idx = _.findIndex($scope.realizationTimes, {ID: elem.ID});
        if(idx > -1) {
          delete $scope.realizationTimes[idx].details;
          Notification.success($filter('translate')('success'));
        }
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });

    }

  })