javascript
import { API } from '@/lib/api';

angular.module('digitalprint.services').service('PsPreflightFolderService', function($rootScope, $q, $http, $config, $cacheFactory) {
  const PsPreflightFolderService = {};
  const cache = $cacheFactory('ps_preflightFolder');

  PsPreflightFolderService.prototype = Object.create(null);

  function PsPreflightFolderService(formatID) {
    this.formatID = formatID;
    this.resource = 'ps_preflightFolder';
    this.getAllResource = `${this.resource}?formatID=${formatID}`;
  }

  PsPreflightFolderService.prototype.getAll = function(force) {
    const def = $q.defer();
    const _this = this;

    // [BACKEND_ADVICE] This is a heavy logic block.
    $http({
      method: 'GET',
      url: `${API.BASE_URL}${_this.getAllResource}`,
    }).then(
      (response) => def.resolve(response.data),
      (error) => def.reject(error)
    );

    return def.promise;
  };

  PsPreflightFolderService.prototype.getAllCache = function(force) {
    const _this = this;

    if (!force && cache.get(_this.getAllResource)) {
      // [BACKEND_ADVICE] Use cached data here.
      return $q.when(cache.get(_this.getAllResource));
    }

    return new Promise((resolve, reject) => {
      _this.getAll(force).then(
        (data) => {
          cache.put(_this.getAllResource, data);
          resolve(data);
        },
        (error) => reject(error)
      );
    });
  };

  return PsPreflightFolderService;
});
