angular.module('digitalprint.services')
  .factory('OfferService', function($rootScope, Upload, $q, $http, $config, $cacheFactory){

    var OfferService = {};

    var resource = 'offers';

    var cache = $cacheFactory(resource);

    var getAllDef = null;

    OfferService.getAll = function(filters, force){
      if(_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
        getAllDef = $q.defer();
      } else {
        return getAllDef.promise;
      }

      var url = resource;

      var qs = $.param(filters || {});
      if(qs) {
        url += '?' + qs;
      }

      // przez filtr cache nie działa.
      if(false && cache.get('collection') && !force) {
        getAllDef.resolve(cache.get('collection'));
      } else {
        $http({
          method: 'GET',
          url: $config.API_URL + url
        }).success(function(data) {
          cache.put('collection', data);
          getAllDef.resolve(data);
        }).error(function(data) {
          getAllDef.reject(data);
        });
      }

      return getAllDef.promise;
    }

    OfferService.getCurrent = function() {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + [resource, 'getCurrent'].join('/')
      }).success(function(data) {
        if(_.isArray(data) && data.length === 0) {
          data = false;
        }
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.addItem = function(item) {
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + 'offerItems',
        data: item
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.uploadItemFile = function(offerItemID, file) {

      return Upload.upload({
        url: $config.API_URL + ['offerItems', 'files', offerItemID].join('/'),
        fileFormDataName: 'itemFile',
        file: file
      });
    }

    OfferService.getItemFiles = function(offerItemID) {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + ['offerItems', 'files', offerItemID].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.getFile = function(fileID, fromCompanyID) {
      // return file link resource
      var addStr = '';
      if( typeof fromCompanyID !== 'undefined' ){
        addStr = '?fromCompanyID=' + fromCompanyID;
      }
      return $config.API_URL + ['offerItems', 'getFile', fileID].join('/') + addStr;
    }

    OfferService.removeItemFile = function(fileID) {
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + ['offerItems', 'files', fileID].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.removeItem = function(id) {
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + ['offerItems', id].join('/')
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.getCompanies = function() {
      //offerCompanies
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + 'offerCompanies'
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.create = function(data){
      var def = $q.defer();

      $http({
        method: 'POST',
        url: $config.API_URL + resource,
        data: data
      }).success(function(data) {
        if(data.ID) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.update = function(offer){
      var def = $q.defer();

      $http({
        method: 'PUT',
        url: $config.API_URL + resource,
        data: offer
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    // remove by ID
    OfferService.remove = function(id){
      var def = $q.defer();

      $http({
        method: 'DELETE',
        url: $config.API_URL + [resource, id].join("/")
      }).success(function(data) {
        if(data.response) {
          cache.remove('collection');
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.userCanAddFile = function() {
      var def = $q.defer();

      $http({
        method: 'GET',
        url: $config.API_URL + ['offerItems', 'userCanAddFile'].join('/')
      }).success(function(data) {
        def.resolve(data);
      }).error(function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    OfferService.toggleVisible = function(fileID, data) {

    var def = $q.defer();

    $http({
      method: 'PUT',
      url: $config.API_URL + ['offerItems', 'files', fileID].join('/'),
      data: data
    }).success(function(data) {
      if(data.response) {
        def.resolve(data);
      } else {
        def.reject(data);
      }
    }).error(function(data) {
      def.reject(data);
    });

    return def.promise;
  }

    return OfferService;
  });
