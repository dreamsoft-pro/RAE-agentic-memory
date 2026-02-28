angular.module('digitalprint.services')
  .service('HelpService', function ($rootScope, $q, Restangular, localStorageService) {

    var HelpService = {};

    HelpService.getQuestion = function (key) {
      var def = $q.defer();

      Restangular.one('adminHelps', key).doGET().then(function(data){
        def.resolve(data.plain());
      }, function(data){
        def.reject(data);
      });

      return def.promise;
    }

    HelpService.getGroup = function (group) {
      var def = $q.defer();

      // Restangular.all('adminHelps', group).doGET().then(function (data) {
      //   def.resolve(data.plain());
      // });

      def.resolve('getGroup');

      return def.promise;
    }


    return HelpService;
  });