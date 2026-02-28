'use strict';

angular.module('paginationAPI')
  .directive('sortbutton', function () {
    return {
      templateUrl: 'views/sortbutton.html',
      restrict: 'AE',
      replace: true,
      scope: {
          settings: '=',
          key: '@'

      },
      link: function (scope, element, attrs) {
          scope._ = _;
      }
    };
  });
