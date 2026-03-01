javascript
import { BackendApi } from '@/lib/api';
import { createDeferred, handleHttpError } from '@/helpers/promise';

angular.module('digitalprint.services')
  .service('PermissionService', function($q, Restangular, $http, $config) {
    const PermissionService = {};

    PermissionService.getAll = () => {
      return BackendApi.aclPermissions.get().then(response => response.plain());
    };

    PermissionService.create = permission => {
      return createDeferred(() =>
        $http.post(`${$config.API_URL}/aclPermissions`, permission)
          .success(data => data)
          .error(handleHttpError)
      ).promise;
    };

    PermissionService.update = permission => {
      const def = $q.defer();
      // [BACKEND_ADVICE] Move heavy logic to backend if necessary.
