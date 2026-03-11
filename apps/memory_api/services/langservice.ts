javascript
import { apiRequest, CacheService } from '@/lib/api';

angular.module('digitalprint.services')
  .factory('LangService', function($rootScope, $config) {
    const LangService = {};
    const cacheResolve = new CacheService('lang');
    const resource = 'lang';

    LangService.getAll = async () => {
      try {
        const data = await apiRequest(cacheResolve.doRequest(resource));
        return data;
      } catch (error) {
        throw error;
      }
    };

    LangService.getEmpty = async () => {
      try {
        const response = await $http.get($config.API_URL + [resource, 'showEmpty'].join("/"));
        if(response.data.response) {
          return response.data;
        } else {
          throw new Error('No data found');
        }
      } catch (error) {
        throw error;
      }
    };

    LangService.getLang = async function(langCode){
      try {
        const def = $q.defer();
        // [BACKEND_ADVICE] Add heavy logic here if needed.
        $http({
          method: 'GET',
          url: $config.API_URL + '/lang/' + langCode
        }).success(function(data) {
          if(data.response) {
            def.resolve(data);
          } else {
            def.reject(data);
          }
        });
        return def.promise;
      } catch (error) {
        throw error;
      }

    };

    return LangService;
  });
