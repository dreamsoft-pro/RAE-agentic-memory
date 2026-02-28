'use strict';

angular.module('digitalprint.services')
  .factory('PsVolumeService', function($q, Restangular, $cacheFactory, $http, $config, PsTypeService) {

    var cache = $cacheFactory('ps_volume')

    var VolumeService = function(groupID, typeID) {
      this.groupID = groupID;
      this.typeID = typeID;
      this.resource = 'ps_groups/'+groupID+'/ps_types/'+typeID+'/ps_volumes';
    }


    VolumeService.prototype.getAll = function(force) {
      var def = $q.defer();
      var _this = this;

      if(cache.get(this.resource) && !force) {
        def.resolve(cache.get(this.resource));
      } else {
        Restangular.all(_this.resource).getList().then(function(data) {
          cache.put(_this.resource, data.plain());
          def.resolve(data.plain());
        }, function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    VolumeService.prototype.add = function(item) {
      var def = $q.defer();
      var _this = this;

      Restangular.all(_this.resource).doPOST(item).then(function(data) {
        if(data.ID) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    VolumeService.prototype.remove = function(item) {
      var def = $q.defer();
      var _this = this;
      
      Restangular.all(_this.resource).one(item.ID+'').remove().then(function(data) {
        if(data.response) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;

    }

    VolumeService.prototype.getCustom = function(force) {
      var def = $q.defer();

      var resource = this.resource + '/customVolume';

      if(cache.get(resource) && !force) {
        def.resolve(cache.get(resource));
      } else {
        Restangular.one(resource).get().then(function(data) {
          cache.put(resource, data.plain());
          def.resolve(data.plain());
        }, function(data) {
          def.reject(data);
        });
      }

      return def.promise;
    }

    VolumeService.prototype.setCustom = function(value) {
      var def = $q.defer();
      var _this = this;

      Restangular.all(_this.resource).patch({
        action: 'setCustomVolume',
        custom: value
      }).then(function(data) {
        if(data.response) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    VolumeService.prototype.setMaxVolume = function(maxVolume) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'POST',
        url: $config.API_URL + _this.resource + '/setMaxVolume',
        data: {maxVolume: maxVolume}
      }).success(function (data) {
        if(data.response) {
          PsTypeService.cacheRemove(_this.groupID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function (data) {
        def.reject(data);
      })

      return def.promise;
    }
    VolumeService.prototype.setStepVolume = function(stepVolume) {
      var def = $q.defer();
      var _this = this;

      $http({
        method: 'POST',
        url: $config.API_URL + _this.resource + '/setStepVolume',
        data: {stepVolume: stepVolume}
      }).success(function (data) {
        if(data.response) {
          PsTypeService.cacheRemove(_this.groupID);
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }).error(function (data) {
        def.reject(data);
      })

      return def.promise;
    }

    VolumeService.prototype.setFormats = function(formatID, formats) {
      var def = $q.defer();
      var _this = this;

      Restangular.all(_this.resource).patch({
        ID: formatID,
        action: 'formats',
        formats: formats
      }).then(function(data) {
        if(data.response) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    VolumeService.prototype.getRtDetails = function(volume) {
      var def = $q.defer();
      var resource = this.resource + '/' + volume.volume + '/ps_rt_details';

      Restangular.all(resource).getList().then(function(data) {
        def.resolve(data);
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    VolumeService.prototype.saveRtDetails = function(volume, item) {
      var def = $q.defer();
      var resource = this.resource + '/' + volume.volume + '/ps_rt_details';

      Restangular.all(resource).patch(item).then(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.resolve(data);
      });

      return def.promise;
    }

    VolumeService.prototype.removeRtDetails = function(volume, item) {
      var def = $q.defer();
      var resource = this.resource + '/' + volume.volume + '/ps_rt_details';

      Restangular.all(resource).one(item.details.ID+'').remove().then(function(data) {
        if(data.response) {
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.resolve(data);
      });

      return def.promise;
    }

    VolumeService.prototype.setInvisible = function(volume) {
      var def = $q.defer();
      var _this = this;

      Restangular.all(_this.resource).patch({
        ID: volume.ID,
        action: 'setInvisibleVolume',
        invisible: !volume.invisible
      }).then(function(data) {
        if(data.response) {
          cache.remove(_this.resource); //usuwamy cache za każdym add, remove
          def.resolve(data);
        } else {
          def.reject(data);
        }
      }, function(data) {
        def.reject(data);
      });

      return def.promise;
    }

    return VolumeService;

  });