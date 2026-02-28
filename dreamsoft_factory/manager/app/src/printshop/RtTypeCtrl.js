angular.module('digitalprint.app')
  .controller('printshop.RtTypeCtrl', function($scope, $filter, $stateParams, $modal, Notification, PsTypeService) {

    var currentGroupID;
    var currentTypeID;

    function init() {
      currentGroupID = $scope.groupID = $stateParams.groupID;
      currentTypeID = $scope.typeID = $stateParams.typeID;

      PsTypeService.getRealizationTimes(currentGroupID, currentTypeID).then(function(data) {
        $scope.realizationTimes = data;
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });

    }

    init();

    $scope.refreshTimes = function() {
      PsTypeService.getRealizationTimes(currentGroupID, currentTypeID, true);
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

            PsTypeService.setRealizationTime(currentGroupID, currentTypeID, $scope.form).then(function(data) {
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

      PsTypeService.removeRealizationTime(currentGroupID, currentTypeID, elem).then(function(data) {
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