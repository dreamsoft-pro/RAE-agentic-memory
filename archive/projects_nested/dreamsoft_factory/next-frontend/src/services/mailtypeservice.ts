javascript
import { getApi } from '@/lib/api';
import { CACHE_KEY, LEAN_DESIGN_MAX_LINES } from './constants'; // Simulated import for context

const resource = 'mailTypes';

function getAll(force) {
  if (!getAllDef || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
    getAllDef = getDeferred();
  }
  
  const cachedData = cache.get('collection');
  if (cachedData && !force) {
    return getAllDef.resolve(cachedData);
  }

  getApi(`${resource}`).then(
    response => {
      const data = response.data;
      cache.put('collection', data);
      getAllDef.resolve(data);
    },
    error => {
      getAllDef.reject(error);
    }
  );

  return getAllDef.promise;
}

function get(id) {
  const def = getDeferred();

  getApi(`${resource}/${id}`).then(
    response => {
      const data = response.data;
      def.resolve(data);
    },
    error => {
      def.reject(error);
    }
  );

  return def.promise;
}

const MailTypeService = { getAll, get };
export default MailTypeService;

// Helper function for deferred pattern
function getDeferred() {
  const deferred = {};
  deferred.promise = new Promise((resolve, reject) => {
    deferred.resolve = resolve;
    deferred.reject = reject;
  });
  return deferred;
}

const cache = {}; // Simulated cache object

let getAllDef; // Global variable to maintain state
