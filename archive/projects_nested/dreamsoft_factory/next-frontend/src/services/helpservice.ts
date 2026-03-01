javascript
import { ApiService } from '@/lib/api';
import localStorageService from 'localStorageService';

angular.module('digitalprint.services')
  .service('HelpService', function ($rootScope, $q) {
    const HelpService = {};

    HelpService.getQuestion = (key) => {
      const def = $q.defer();

      // [BACKEND_ADVICE] Fetch question details based on key.
      ApiService.doGET(`adminHelps/${key}`).then(
        (response) => { 
          def.resolve(response.data.plain());
        },
        (errorResponse) => { 
          def.reject(errorResponse);
        }
      );

      return def.promise;
    };

    HelpService.getGroup = (group) => {
      const def = $q.defer();

      // [BACKEND_ADVICE] Fetch help group details based on group.
      ApiService.doGET(`adminHelps/group/${group}`).then(
        (response) => { 
          def.resolve(response.data.plain());
        },
        () => { 
          def.reject('Failed to fetch group data.');
        }
      );

      return def.promise;
    };

    return HelpService;
  });
