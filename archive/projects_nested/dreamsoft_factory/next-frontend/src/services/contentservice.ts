javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

class ContentService {
  constructor(routeID) {
    this.routeID = routeID;
    this.resource = ['routes', routeID, 'mainContents'].join('/');
    this.getAllDef = null; // [BACKEND_ADVICE]
  }

  getAll(force) { // [BACKEND_ADVICE]
    return new Promise((resolve, reject) => {
      BackendApi.get(this.resource)
        .then(response => resolve(response.data))
        .catch(error => reject(error));
    });
  }

  getAllCache(force) {
    if (_.isNull(this.getAllDef) || force || this.getAllDef.promise.$$state.status === 1) {
      this.getAllDef = $q.defer();
      this.getAll(true).then(data => {
        this.getAllDef.resolve(data);
      }).catch(error => {
        this.getAllDef.reject(error);
      });
    }
    return this.getAllDef.promise;
  }
}

angular.module('digitalprint.services')
  .service('ContentService', ContentService);

export default ContentService;
