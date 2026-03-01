angular.module('digitalprint.helpers')
  .directive('focusOn', function($rootScope) {
    return function(scope, elem, attr) {
      $rootScope.$on('focusOn', function(e, name) {
        if(name === attr.focusOn) {
          elem[0].focus();
          elem[0].select();
        }
      });
    };
});