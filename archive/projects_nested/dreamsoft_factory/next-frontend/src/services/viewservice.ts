javascript
'use strict';

import { API } from '@/lib/api';
import { BACKEND_ADVICE } from './constants'; // [BACKEND_ADVICE]

angular.module('digitalprint.services')
  .service('ViewService', function($q, $config) {
    var ViewService = function(routeID, viewID) {
      this.routeID = routeID;
      this.viewID = viewID;
    };

    ViewService.prototype.getResource = function() {
      return 'dp_views';
    };

    ViewService.prototype.getAll = function() {
      const def = $q.defer();
      const resource = this.getResource();

      API.get(`${resource}?routeID=${this.routeID}`)
        .then(data => def.resolve(data))
        .catch(error => def.reject(error));

      return def.promise;
    };

    ViewService.prototype.makeViewReplace = function(replaceID) {
      const def = $q.defer();
      const resource = this.getResource();
      const data = {
        replaceID: replaceID, 
        routeID: this.routeID
      };
