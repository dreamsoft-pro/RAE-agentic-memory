'use strict';

angular.module('digitalprint.helpers')
  .filter('offset', function () {
    return function (input, start) {
      start = +start //parse to int
      
      var result = input || [];
      
      return result.slice(start);
    };
  });
