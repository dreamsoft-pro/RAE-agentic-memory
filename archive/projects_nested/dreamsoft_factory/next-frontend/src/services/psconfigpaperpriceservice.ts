javascript
'use strict';

import { BackendService } from '@/lib/api';
import _ from 'lodash';

const cache = $cacheFactory('ps_paperPrice');
let resource;

class PsConfigPaperPrice {
  constructor(attrID, optID) {
    this.attrID = attrID;
    this.optID = optID;
    this.setResource();
    getAllDef = null; // Reset the deferred object
  }

  getResource() {
    return resource;
  }

  setResource() {
    resource = ['ps_attributes', this.attrID, 'ps_options', this.optID, 'paperPrice'].join('/');
    return true;
  }

  getAll(force) {
    if (_.isNull(getAllDef) || force || (getAllDef.promise && getAllDef.promise.$$state.status === 1)) {
      getAllDef = $q.defer();
    } else {
      return getAllDef.promise;
    }
