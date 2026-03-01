angular.module('digitalprint.app')
  .controller('superadmin.LangsRootEmptyCtrl', function($scope, $rootScope, $filter, $modal, LangRootService, LangSettingsRootService, Notification){

    /**
      LangRoot
    **/
    
    $scope.langs;
    $scope.pagination = {
      perPage: 25,
      currentPage: 1
    };
    $scope.filterData = {};

    $scope.pagination.setPage = function(pageNo) {
      $scope.pagination.currentPage = pageNo;
    }

    LangRootService.getEmpty().then(function(data){
      $scope.langs = data;

      $scope.filterLangs = _.clone($scope.langs);

    });


    $scope.search = function(setFirstPage) {
      if(_.isUndefined(setFirstPage)) {
        setFirstPage = true;
      }
      var filterData = _.clone($scope.filterData);

      _.each(filterData, function(item, idx) {

        if(item === true) {
          filterData[idx] = null;
        } else {
          filterData[idx] = '';
        }
      });

      $scope.filterLangs = $filter('filter')(
        $scope.langs,
        filterData
      );
      if(setFirstPage) {
        $scope.pagination.setPage(1);
      }
    }



  });