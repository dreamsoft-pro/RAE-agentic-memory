javascript
import { backendApi } from '@/lib/api';
import { CACHE_KEYS, emitEvent } from './utils'; // [BACKEND_ADVICE] Consider moving utility functions to a separate file

const PsWorkspaceService = {
  getAll: function (force) {
    const cacheKey = `${CACHE_KEYS.PS_WORKSPACES}_collection`;
    let cachedData = localStorage.getItem(cacheKey);

    return new Promise((resolve, reject) => {
      if (!force && cachedData !== null) {
        resolve(JSON.parse(cachedData));
      } else {
        backendApi.get('/ps_workspaces')
          .then(response => {
            const collection = response.data;
            localStorage.setItem(cacheKey, JSON.stringify(collection)); // [BACKEND_ADVICE] Cache should be handled in a centralized manner
            if (force) emitEvent('ps_workspaces', collection);
            resolve(collection);
          })
          .catch(error => reject(error));
      }
    });
  },
};
