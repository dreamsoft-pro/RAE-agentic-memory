javascript
import { BackendService } from '@/lib/api';
import _ from 'lodash';

const AdminHelpService = {};

const resource = 'adminHelps';
const cacheKey = 'collection';

AdminHelpService.getAll = function(force) {
  if (_.isNull(AdminHelpService.getAllDef) || force || (AdminHelpService.getAllDef && AdminHelpService.getAllDef.promise.$$state.status === 1)) {
    AdminHelpService.getAllDef = BackendService.defer();
  } else {
    return AdminHelpService.getAllDef.promise;
  }

  const cachedData = cache.get(cacheKey);
  if (cachedData && !force) {
    console.log('from cache');
    AdminHelpService.getAllDef.resolve(cachedData);
  } else {
    BackendService.get(resource).then(
      data => {
        cache.put(cacheKey, data);
        AdminHelpService.getAllDef.resolve(data);
      },
      error => {
        AdminHelpService.getAllDef.reject(error);
      }
    );
  }

  return AdminHelpService.getAllDef.promise;
};

AdminHelpService.getAllDef = null;

export { AdminHelpService };
