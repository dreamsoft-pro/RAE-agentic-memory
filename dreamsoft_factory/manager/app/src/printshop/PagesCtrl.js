'use strict';

angular.module('digitalprint.app')
  .controller('printshop.PagesCtrl', function($scope, $filter, $stateParams, Notification, PsPageService){
    var currentGroupID;
    var currentTypeID;

    currentGroupID = $scope.currentGroupID = $stateParams.groupID;
    currentTypeID = $scope.currentTypeID = $stateParams.typeID;

    var PageService = new PsPageService(currentGroupID, currentTypeID);

    PageService.getAll().then(function(data) {
      $scope.pages = [];
      if(!data.length) {
        return;
      }
      if(_.first(data).minPages) {
        $scope.pages = _.first(data);
        $scope.rangePages = true;
      } else {
        $scope.pages = data;
        $scope.rangePages = false;
      }
    });

    $scope.resetForm = function() {
      $scope.form = {};
      $scope.form.range = false;
    }

    $scope.resetForm();

    $scope.add = function(form) {

      if(form.range) {
        form.action = 'range';
      } else {
        form.action = 'pages';
      }
      delete form.range;

      PageService.addPage(form).then(function(data) {
        if(form.action === 'pages') {
          if($scope.rangePages) {
            $scope.pages = {};
          }
          $scope.pages.push(data.item);
          $scope.rangePages = false;
        } else {
          $scope.pages = {};
          $scope.pages = data.item;
          $scope.rangePages = true;
        }
        $scope.resetForm();
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error')+ " " +data.error);
      });

    }

    $scope.setSimilarPage = function() {
      PageService.setSimilarPage($scope.similarPage).then(function(data) {
        Notification.success($filter('translate')('success'));
      }, function(data) {
        Notification.error($filter('translate')('error'));
      });
    }

    $scope.remove = function(item) {
      PageService.remove(item).then(function(data) {
        if($scope.rangePages) {
          $scope.pages = [];
          $scope.rangePages = false;
        } else {
          var idx = _.findIndex($scope.pages, {ID: item.ID});
          if(idx > -1) {
            $scope.pages.splice(idx, 1);
            Notification.success($filter('translate')('success'));
          }
        }
      });
    }


  });