javascript
import { API } from '@/lib/api';
import { LeanService } from '@/utils/lean-service';

class CountriesService extends LeanService {
  getResource() {
    // [BACKEND_ADVICE] This method returns the resource path for countries data.
    return ['dp_countries'].join('/');
  }

  getAll() {
    const deferred = this.$q.defer();

    const resource = this.getResource();
    const url = API.getApiUrl() + resource;

    this.$http.get(url).then(
      (response) => {
        // [BACKEND_ADVICE] Success response handling.
        deferred.resolve(response.data);
      },
      (error) => {
        // [BACKEND_ADVICE] Error response handling.
        deferred.reject(error);
      }
    );

    return deferred.promise;
  }
}

export const countriesService = new CountriesService($rootScope, $q, $config, $http);
