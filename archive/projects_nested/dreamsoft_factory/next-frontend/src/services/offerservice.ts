javascript
import { BackendApi } from '@/lib/api';
import _ from 'lodash';

const OfferService = {};

const resource = 'offers';
const cache = new Map();

let getAllDef = null;

OfferService.getAll = function(filters, force) {
  if (_.isNull(getAllDef) || force || (getAllDef && getAllDef.promise.$$state.status === 1)) {
    getAllDef = Promise.resolve();
  } else {
    return getAllDef.promise;
  }

  const url = resource;

  let qs = '';
  if (!_.isEmpty(filters)) {
    qs = new URLSearchParams(filters).toString();
  }
  if (qs) {
    url += '?' + qs;
  }

  // [BACKEND_ADVICE] Fetch offers from backend
  BackendApi.get(url)
    .then(response => {
      getAllDef.resolve(response.data);
    })
    .catch(error => {
      getAllDef.reject(error);
    });

  return getAllDef.promise;
};

export { OfferService };
