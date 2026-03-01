javascript
import { BackendApi } from '@/lib/api';
import { createDeferredPromise } from '@/utils/promiseUtils';

angular.module('digitalprint.services')
    .service('UserAddressService', function ($q, $http, $config) {
        
        // [BACKEND_ADVICE] Consider moving heavy logic to backend service.

        class UserAddressService {
            constructor(userID) {
                this.userID = userID;
                this.resource = ['users', this.userID, 'address'].join('/');
            }

            getAllAddresses() {
                const def = createDeferredPromise();
                
                $http({
                    method: 'GET',
                    url: $config.API_URL + this.resource + '?type=1'
                }).success((data) => {
                    def.resolve(data);
                }).error((data) => {
                    def.reject(data);
                });

                return def.promise;
            }
        }

        // [BACKEND_ADVICE] This service could benefit from backend support for complex logic handling.
        
        angular.module('digitalprint.services').factory('UserAddressService', ['$q', '$http', '$config', function ($q, $http, $config) {
            class UserAddressService {
                constructor(userID) {
                    this.userID = userID;
                    this.resource = ['users', this.userID, 'address'].join('/');
                }

                getAllAddresses() {
                    const def = createDeferredPromise();

                    $http({
                        method: 'GET',
                        url: $config.API_URL + this.resource + '?type=1'
                    }).success((data) => {
                        def.resolve(data);
                    }).error((data) => {
                        def.reject(data);
                    });

                    return def.promise;
                }
            }

            return new UserAddressService($config.USER_ID);
        }]);
    });
