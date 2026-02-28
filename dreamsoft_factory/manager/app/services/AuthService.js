/**

 AuthServiece, AuthDataService

 **/

angular.module('digitalprint.services')
    .factory('AuthDataService', function ($rootScope, $cookieStore, localStorageService, $config) {

        var AuthDataService = {};

        var accessTokenName = $config.ACCESS_TOKEN_NAME;

        AuthDataService.setUserData = function (data) {
            $rootScope.username = data.user.firstname;
            localStorageService.set('user', data.user);
            this.setAccessToken(data.token || data[$config.API_ACCESS_TOKEN_NAME]);
            $rootScope.$emit('Auth:userData');
        };

        AuthDataService.destroyUserData = function () {
            delete $rootScope.username;
            this.deleteAccessToken();
            localStorageService.remove('user');
            localStorageService.remove('domainID');
        };

        AuthDataService.logout = function () {
            this.destroyUserData();
            $rootScope.$emit("Auth:loggedOut");
        };

        AuthDataService.getCurrentUser = function () {
            return localStorageService.get('user');
        };

        AuthDataService.getAccessToken = function () {
            function getCookie(cname) {
                var name = cname + "=";
                var decodedCookie = decodeURIComponent(document.cookie);
                var ca = decodedCookie.split(';');
                for (var i = 0; i < ca.length; i++) {
                    var c = ca[i];
                    while (c.charAt(0) == ' ') {
                        c = c.substring(1);
                    }
                    if (c.indexOf(name) == 0) {
                        return c.substring(name.length, c.length);
                    }
                }
                return "";
            }

            return getCookie(accessTokenName);
        };

        AuthDataService.setAccessToken = function (accessToken) {
            var domainName = window.location.hostname;

            var expiration_date = new Date();
            expiration_date.setFullYear(expiration_date.getFullYear() + 1);

            document.cookie = accessTokenName + "=" + accessToken + "; domain=" + domainName + "; path=/; expires=" +
                expiration_date.toUTCString();
        };

        AuthDataService.deleteAccessToken = function () {
            var domainName = window.location.hostname;
            document.cookie = accessTokenName + "=" + "; domain=" + domainName + "; path=/" + ";expires=-1";
        };

        AuthDataService.isLoggedIn = function () {
            return this.getAccessToken();
        };

        return AuthDataService;
    });

angular.module('digitalprint.services')
    .factory('AuthService', function ($rootScope, $q, $config, $http, AuthDataService) {
        var AuthService = {};
        AuthService = _.merge(AuthService, AuthDataService);

        AuthService.loginNew = function (credentials) {
            var _this = this;
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.AUTH_URL + 'login',
                data: $.param(credentials),
                params: {
                    domainName: location.hostname
                },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            }).success(function (data) {
                _this.setUserData(data);
                def.resolve(data);
                $rootScope.$emit("Auth:loggedIn");
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuthService.login = function (credentials) {
            var _this = this;
            var def = $q.defer();

            $http({
                method: 'POST',
                url: $config.AUTH_URL + 'login',
                data: $.param(credentials),
                params: {
                    domainName: location.hostname
                },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            }).success(function (data) {
                _this.setUserData(data);
                def.resolve(data);
                $rootScope.$emit("Auth:loggedIn");
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuthService.logout = function () {
            var _this = this;
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + ['auth', 'logout'].join('/')
            }).success(function (data) {

                $rootScope.$emit("Auth:loggedOut");
                _this.destroyUserData();
                def.resolve(data);
            }).error(function (data) {
                def.reject(data);
            });
            return def.promise;
        };

        AuthService.check = function () {
            var _this = this;
            var def = $q.defer();

            $http({
                method: 'GET',
                url: $config.API_URL + ['auth', 'check'].join('/')
            }).success(function (data) {
                if (data.response) {
                    AuthDataService.setUserData(data);
                    def.resolve(data);
                } else {
                    def.reject(data);
                }
            }).error(function (data) {
                def.reject(data);
            });

            return def.promise;
        };

        AuthService.restoreSession = function () {
            var accessToken = this.getAccessToken();
        };

        return AuthService;
    });
