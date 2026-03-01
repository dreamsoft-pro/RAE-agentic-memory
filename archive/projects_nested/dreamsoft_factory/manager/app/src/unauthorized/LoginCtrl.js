// used in unauthorized and base view
angular.module('digitalprint.app')
    .controller('unauthorized.LoginCtrl', function ($rootScope, $scope, $state, AuthService,
                                                    DomainService, Notification) {

        if (!_.isUndefined($state.current.data)) {
            $rootScope.bodyClass = $state.current.data.bodyClass;
        }

        $scope.customLogo = false;
        if (window.location.href.indexOf('bph.canon-business-services.pl') > -1 ||
            window.location.href.indexOf('707.digitalprint.pro') > -1) {
            $scope.customLogo = 'bph';
        }


        $scope.credentials = {
            email: 'admin',
            password: ''
        };

        $scope.domains = [];

        $rootScope.rememberLogin = false;

        function init() {

            DomainService.getAll().then(function(data) {

                $scope.domains = data;

            });

        }

        $scope.login = function (credentials) {
            AuthService.login(credentials).then(function (data) {
                $rootScope.logged = true;

                if( credentials.domainID ) {
                    DomainService.setDomain(credentials.domainID);
                } else {
                    DomainService.getCurrentDomain();
                }

                Notification.success("Login success");
                $state.go('shop-base');
                setTimeout(function () {
                    jQuery(function () {
                        Metronic.init();
                        Layout.init();
                        QuickSidebar.init();
                    });
                }, 1000);
            }, function (data) {
                $rootScope.logged = false;
                if (data.httpCode === 400) {
                    Notification.error("Błąd logowania - zły login lub hasło")
                } else {
                    Notification.error("Error " + data.error);
                }
            });
        };

        $scope.logout = function () {
            AuthService.logout().then(function () {
            }, function (data) {
                $scope.check();
            });
        };

        $scope.check = function () {
            AuthService.check().then(function (data) {
                $rootScope.logged = true;
            }, function (data) {
                $rootScope.logged = false;
            });
        };

        $scope.getUser = function () {
            return AuthService.getCurrentUser();
        };

        $rootScope.$on('Auth:loggedOut', function () {
            $rootScope.logged = false;
            $state.go('login');
        });

        init();

    });