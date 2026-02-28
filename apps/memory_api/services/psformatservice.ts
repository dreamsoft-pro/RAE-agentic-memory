javascript
'use strict';

import { createBackendApi } from '@/lib/api';
const backendApi = createBackendApi();

angular.module('digitalprint.services')
    .factory('PsFormatService', function ($q, Restangular, $cacheFactory) {

        const cache = $cacheFactory('ps_formats');

        class FormatService {
            constructor(groupID, typeID) {
                this.groupID = groupID;
                this.typeID = typeID;
            }

            getResource() {
                return 'ps_groups/' + this.groupID + '/ps_types/' + this.typeID + '/ps_formats';
            }

            getPublic(complexID, force) {
                const def = $q.defer();
                const _this = this;

                const resource = _this.getResource() + '/formatsPublic/' + complexID;
                
                // [BACKEND_ADVICE] Fetch public formats from backend.
                backendApi.get(resource, { cache: !force })
                    .then(response => {
                        def.resolve(response);
                    }, error => {
                        def.reject(error);
                    });

                return def.promise;
            }
        }

        return FormatService;
    });
