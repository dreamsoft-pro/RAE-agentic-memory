angular.module('digitalprint.helpers')
  .factory('focus', function ($rootScope, $timeout) {
  return function(name) {
    $timeout(function (){
      $rootScope.$emit('focusOn', name);
    });
  }
});