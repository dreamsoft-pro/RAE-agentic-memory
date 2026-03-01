javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

const resource = 'skills';

const cache = new Map();

let getAllDef = null;

export const SkillService = {
  async getAll(force = false) {
    if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
      getAllDef = Promise.defer();
    } else {
      return getAllDef.promise;
    }

    if (!force && cache.get('collection')) {
      getAllDef.resolve(cache.get('collection'));
    } else {
      BackendApi.get(`${resource}`).then(data => {
        cache.set('collection', data);
        getAllDef.resolve(data);
      }).catch(data => {
        getAllDef.reject(data);
      });
    }

    return getAllDef.promise;
  },

  devices(skill) {
    const def = Promise.defer();
    // [BACKEND_ADVICE] Add backend logic here
    return def.promise;
  }
};
