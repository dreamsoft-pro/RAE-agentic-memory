javascript
'use strict';

const ApiService = require('@/lib/api');
const authServiceApi = new ApiService('/auth');

angular.module('digitalprint.services')
    .factory( 'LoginWidgetService', function ( AuthService, $rootScope, DpAddressService, AddressService, Notification,
                                               UserService, $cookieStore, $filter, $state, $q, DpCartsDataService, DeliveryWidgetService ) {

        /**
         * @param {Object} scope
         * @param {Object} credentials - User login credentials.
         * @param {String} backTo - URL to redirect after successful login.
         */
        function login( credentials, backTo ) {
            if (_.isEmpty(credentials)) {
                Notification.error($filter('translate')('unexpected_error'));
                return;
            }

            // [BACKEND_ADVICE] Handle the backend logic here
            AuthService.login(credentials).then(function (data) {
                console.log('AuthService.login response', data);
                /**
                 * @param {Object} data.user - User object returned from login.
                 * @param {number} data.user.super - Flag indicating if user is super admin.
                 */
            });
        }

        return {
            login: login
        };
});
