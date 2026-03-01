javascript
import { API } from '@/lib/api';
import localStorageService from 'localStorageService';
import Notification from 'Notification';
import TokenService from 'TokenService';
import AuthDataService from 'AuthDataService';
import AuthService from 'AuthService';
import $filter from '$filter';
import $q from '$q';

const LogoutService = {
  destroyUserData: () => {
    delete $rootScope.username;
    AuthDataService.deleteAccessToken();
    localStorageService.remove('user');
    return true;
  },

  logout: function() {
    return this.destroyUserData();
  },

  init: function() {
    const def = $q.defer();

    AuthDataService.logout();
    Notification.info($filter('translate')('you_are_loggedout'));
    
    // [BACKEND_ADVICE] Heavy logic for getting non-user token should be moved to backend if possible.
    TokenService.getNonUserToken().then((data) => {
      AuthService.setAccessToken(data.token);
      def.resolve(true);
    });

    return def.promise;
  }
};

export default LogoutService;
