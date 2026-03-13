'use strict';

angular.module('digitalprint.helpers')
  .filter('ids', function () {
    return function (input, ids) {
      // console.log('filter', input, ids);
      var result =[];
      
      _.each(input, function(item, key) {
        var idx = _.findIndex(ids, {ID: item.ID});
        if(idx > -1) {
          result.push(item);
        }
      });
      return result;
    };
  });
