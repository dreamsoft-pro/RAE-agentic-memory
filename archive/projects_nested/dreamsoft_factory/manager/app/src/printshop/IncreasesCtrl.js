'use strict';

angular.module('digitalprint.app')
  .controller('printshop.IncreasesCtrl', function(increaseTypes, $scope, $filter, $stateParams, Notification,
                                                  PsIncreaseService, PsIncreaseTypeService, PsFormatService){
    var currentGroupID;
    var currentTypeID;

    currentGroupID = $scope.currentGroupID = $stateParams.groupID;
    currentTypeID = $scope.currentTypeID = $stateParams.typeID;

    var IncreaseService = new PsIncreaseService(currentGroupID, currentTypeID);

    $scope.formats = [];
    var FormatService = new PsFormatService(currentGroupID, currentTypeID);
    FormatService.getAll().then(function(data) {
      $scope.formats = data;
    }, function(data) {
      Notification.error($filter('translate')('error'));
    });

    $scope.resetForm = function() {
      $scope.form = {};
      $scope.form.type = _.first($scope.increaseTypes).ID;
    }
    $scope.resetInputForm = function(form) {
      form.amount = '';
      form.value = '';
    }
    $scope.selectIncreaseType = function(type) {
      $scope.currentIncreaseType = null;
      $scope.increaselist = [];
      // console.log('currentType', type)
      IncreaseService.getAll(type.ID).then(function(data) {
        $scope.increaselist = data;
      });
      $scope.currentIncreaseType = type;
      $scope.resetForm();
    }

    $scope.increaseTypes = increaseTypes;
    $scope.selectIncreaseType($scope.increaseTypes[0]);


    $scope.save = function(form) {
      form.type = $scope.currentIncreaseType.ID;

      IncreaseService.save(form).then(function(data) {
        // nowy element
        if(data.info !== "update" && data.item.ID) {
          var increaselistExists = false;
          // console.log()
          _.each($scope.increaselist, function(list) {
            if(_.first(list).formatID === data.item.formatID) {
              list.push(data.item);
              $scope.resetInputForm(form);
              $scope.resetForm();
              Notification.success($filter('translate')('success'));
              increaselistExists = true;
              return false;
            }
          });

          // console.log(increaselistExists);

          if(!increaselistExists) {
            $scope.increaselist.push([data.item]);
            $scope.resetInputForm(form);
            $scope.resetForm();
            Notification.success($filter('translate')('success'));
          }
        } else if(data.info === "update" && data.item.ID) {
          _.each($scope.increaselist, function(list, i) {
            var idx = _.findIndex(list, {amount: data.item.amount, formatID: data.item.formatID});
            // console.log(idx);
            if(idx > -1) {
              list[idx] = data.item;
              $scope.resetInputForm(form);
              $scope.resetForm();
              Notification.success($filter('translate')('success'));
              return false;
            }

          });
        }
      }, function(data) {
        Notification.error($filter('translate')('error')+ " " +data.error);
      });

    }

    $scope.remove = function(item) {
      IncreaseService.remove(item).then(function(data) {
        _.each($scope.increaselist, function(list, i) {
          var idx = list.indexOf(item);
          if(idx > -1) {
            list.splice(idx, 1);
            if(!$scope.increaselist[i].length) {
              $scope.increaselist.splice(i, 1);
            }
            Notification.success($filter('translate')('success'));
            return false;
          }
        });
        
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }


  });
