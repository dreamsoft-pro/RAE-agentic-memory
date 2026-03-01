angular.module('digitalprint.config', []);
angular.module('digitalprint.routes', ['ui.router', 'restangular']);
angular.module('digitalprint.directives', []);
angular.module('digitalprint.services', ['LocalStorageModule']);
angular.module('digitalprint.helpers', ['ui-notification']);
angular.module('dreamsoft.tinymce', []);

angular.module('digitalprint.app', [
    'LocalStorageModule',
    'ui.bootstrap',
    'pascalprecht.translate',
    'ngCookies',
    'ngAnimate',
    'angular-api-collection',
    'ui.sortable',
    'ncy-angular-breadcrumb',
    'textAngular',
    'btford.socket-io',
    'angularFileUpload',
    'paginationAPI',
    'ngFileUpload',
    'colorpicker.module',
    'digitalprint.routes',
    'digitalprint.directives',
    'digitalprint.services',
    'digitalprint.helpers',
    'digitalprint.config',
    'rzSlider',
    'dreamsoft.tinymce'
])
    .config(function ($provide, $configProvider, RestangularProvider, localStorageServiceProvider,
                      ApiCollectionProvider, $breadcrumbProvider, $httpProvider) {

        var mainUrl = 'REPLACE_API_URL';
        var mainUrlTest = 'REPLACE-API-URL';

        if (mainUrl === mainUrlTest.replace(/\-/g, '_')) {
            $configProvider.set('API_URL', 'http://localhost:8081/api/');
            RestangularProvider.setBaseUrl('http://localhost:8081/api/');
        } else {
            $configProvider.set('API_URL', mainUrl);
            RestangularProvider.setBaseUrl(mainUrl);
        }

        var authUrl = 'REPLACE_AUTH_URL';
        var authUrlTest = 'REPLACE-AUTH-URL';

        if (authUrl === authUrlTest.replace(/\-/g, '_')) {
            $configProvider.set('AUTH_URL', 'http://authapp.localhost:8081/');
        } else {
            $configProvider.set('AUTH_URL', authUrl);
        }

        var staticUrl = 'REPLACE_STATIC_URL';
        var staticUrlTest = 'REPLACE-STATIC-URL';

        if (staticUrl === staticUrlTest.replace(/\-/g, '_')) {
            $configProvider.set('STATIC_URL', 'http://localhost:8081/static/');
        } else {
            $configProvider.set('STATIC_URL', staticUrl);
        }

        var socketUrl = 'REPLACE_SOCKET_URL';
        var socketUrlTest = 'REPLACE-SOCKET-URL';

        if (socketUrl === socketUrlTest.replace(/\-/g, '_')) {
            $configProvider.set('SOCKET_URL', 'http://authapp.localhost:8081/');
        } else {
            $configProvider.set('SOCKET_URL', socketUrl);
        }

        var editorUrl = 'REPLACE_EDITOR_URL';
        var editorUrlTest = 'REPLACE-EDITOR-URL';

        if (editorUrl === editorUrlTest.replace(/\-/g, '_')) {
            $configProvider.set('EDITOR_URL', 'http://editor.localhost:8081/');
        } else {
            $configProvider.set('EDITOR_URL', editorUrl+'indexa.html');
        }

        $configProvider.set('ACCESS_TOKEN_NAME', 'manager-access-token');
        $configProvider.set('API_ACCESS_TOKEN_NAME', 'access-token');

        RestangularProvider.setMethodOverriders(['put', 'patch']);

        localStorageServiceProvider.setPrefix('digitalprint');

        $breadcrumbProvider.setOptions({
            includeAbstract: true
        });

        $httpProvider.interceptors.push('authInterceptor');
        $httpProvider.interceptors.push('httpMethodOverride');
        $httpProvider.interceptors.push('loadingInterceptor');
        $httpProvider.interceptors.push('catchMailErrorInterceptor');
        $httpProvider.interceptors.push('responseErrorInterceptor');

    })
    .run(function ($rootScope, $state, AuthService, DomainService, ApiCollection) {
        $rootScope.parseInt = window.parseInt; window.alert=function(){console.log('alert removed')};
        $rootScope.$state = $state;

        $rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
            if (toState.name != 'login' && $rootScope.logged === false) {
                event.preventDefault();
                $state.go('login');
            }
            console.info('newState',{toState: toState, toParams: toParams});
        });

        $rootScope.$on('$viewContentLoaded', function (event) {

            $('.wrapper1').on('scroll', function (e) {
                $('.wrapper2').scrollLeft($('.wrapper1').scrollLeft());
            });
            $('.wrapper2').on('scroll', function (e) {
                $('.wrapper1').scrollLeft($('.wrapper2').scrollLeft());
            });
            var div = $('.div1');
            div.width((div.parent().next().find("table")).width());
            $('.div2').width($('table').width());
        });

    })
    .factory('httpMethodOverride', function () {
        return {
            'request': function (config) {
                if (config.method === 'PUT' || config.method === 'PATCH') {
                    config.headers['x-http-method-override'] = config.method.toLowerCase();
                    config.method = 'POST';
                }
                return config;
            }

        };
    })
    .factory('authInterceptor', function ($q,
                                          $location,
                                          AuthDataService,
                                          $cookieStore,
                                          localStorageService,
                                          $rootScope,
                                          $config) {
        return {
            request: function (config) {

                config.headers = config.headers || {};

                if (AuthDataService.getAccessToken()) {
                    config.headers[$config.API_ACCESS_TOKEN_NAME] = AuthDataService.getAccessToken();
                }

                if (localStorageService.get('domainID')) {
                    config.headers.domainID = localStorageService.get('domainID');
                } else {
                    console.log('Brak domeny');
                }
                config.headers.sourceApp = 'manager';

                return config;
            },
            responseError: function (rejection) {
                if (rejection.status === 401 || rejection.status === 403) {
                    AuthDataService.destroyUserData();
                    $location.path('/login');
                    console.log('redirect to login');
                }
                if( typeof rejection !== 'object') {
                    AuthDataService.destroyUserData();
                    $location.path('/login');
                    console.log('bad token detected');
                    return $q.reject({});
                }
                return $q.reject(rejection);
            }
        };
    })
    .factory('loadingInterceptor', function ($q, LoadingService) {
        return {
            request: function (config) {
                LoadingService.requested();
                config.requestTimestamp = new Date().getTime();
                return config;
            },
            response: function (response) {
                LoadingService.responsed();
                return response;
            },
            responseError: function (rejection) {
                LoadingService.responsed();
                return $q.reject(rejection);
            }
        }
    })
    .factory('catchMailErrorInterceptor', function () {
        return {
            response: function (response) {
                if (response.data.mailInfo && response.data.mailInfo.error) {
                    alert('Mail Error: ' + response.data.mailInfo.error);
                    console.log('Mail Error: ' + response.data.mailInfo.error);
                }
                return response;
            }
        }
    })
    .factory('responseErrorInterceptor', function ($q, $injector, $timeout) {
        return {
            responseError: function (response) {
                console.log('responseError Status: ' + response.status);

                if (response.status === 0 || response.status === 408 || response.status > 500) {
                    var $http = $injector.get('$http');
                    return $timeout(function () {
                        return $http(response.config);
                    }, 3000, false);
                } else {
                    return $q.reject(response);
                }

            }
        }
    }).factory('socket', function (socketFactory, $config) {

    var myIoSocket = io.connect($config.SOCKET_URL, {secure: true});

    var mySocket = socketFactory({
        prefix: '',
        ioSocket: myIoSocket
    });

    mySocket.forward('error');
    return mySocket;
});

var scrollPosition_before = 0;
var breadcrumbWidth;

var scrolling = function () {

    var menu = $('div.page-sidebar.navbar-collapse.collapse');
    var menuBottom = menu.position().top + menu.innerHeight();
    var menuTop = menu.position().top;
    var innerHeight = $(window).innerHeight();
    var inerBottom = ($(document).scrollTop()) + ($(window).innerHeight());
    var sidebarTop = $('.page-header.navbar.navbar-fixed-top');
    var scrollPosition = $(document).scrollTop();

    function menuHeight() {
        return menu.height() + sidebarTop.height();
    }

    if (innerHeight > menuHeight()) {

        menu.addClass('sticky').animate({
            top: "46px"
        }, 0);

        if (($(window).scrollTop() + $(window).innerHeight()) <= (menu.offset().top + menu.innerHeight())) {
            menu.css({
                top: ($(window).innerHeight() - menu.innerHeight())
            });

            if ((menu.offset().top + menu.innerHeight()) > $('.page-footer').offset().top) {
                menu.css({
                    top: $(window).innerHeight() - menu.innerHeight() - $('.page-footer').innerHeight()
                });
            }
        }
        return;
    }

    var diff = parseInt(scrollPosition_before - scrollPosition);

    if (diff > 0) {
        menu.addClass('sticky').css({
            top: parseInt(menu.position().top) + (diff)
        });
        if (menu.position().top > sidebarTop.height()) {
            menu.css({
                top: sidebarTop.height()
            });
        }
        scrollPosition_before = scrollPosition;
        return;
    }

    if (diff < 0) {

        if (innerHeight <= (menu.innerHeight() + sidebarTop.height())) {
            menu.addClass('sticky').css({
                top: parseInt(menu.position().top) + (diff)
            });

            if (($(window).scrollTop() + innerHeight) >= (menu.offset().top + menu.innerHeight())) {

                menu.css({
                    top: (parseInt(menu.position().top)) - (diff)
                });

                // jeśli dolna pozycja okna przeglądarki jest mniejsza lub równa od dolnej pozycji menu
                if (($(window).scrollTop() + innerHeight) <= (menu.offset().top + menu.innerHeight())) {
                    menu.css({
                        top: (innerHeight - menu.innerHeight())
                    });

                    if ((menu.offset().top + menu.innerHeight()) > $('.page-footer').offset().top) {
                        menu.css({
                            top: innerHeight - menu.innerHeight() - $('.page-footer').innerHeight()
                        });
                    }
                }

            }

        }

        scrollPosition_before = scrollPosition;

    }
};

$(window).on('scroll', scrolling);

$(window).on('resize', function () {

    scrolling();

    $(window).off('scroll', scrolling);
    $(window).on('scroll', scrolling);

});

var breadcrumbScroll = function () {

    var breadcrumbPosition = $('ol.breadcrumb').position().top;
    var scroll = $(document).scrollTop();
    var newPosition = $(document).height() - $('.page-content-wrapper').height() - 30;
    breadcrumbWidth = $('.ui-view-animate.fadeInOut').width();


    if ($('div.hiddenDiv').length == 0) {
        $('.page-title').append("<div class='hiddenDiv'></div>");
    }

    $('ol.breadcrumb').css({
        width: breadcrumbWidth + "px"
    });

    if (scroll > breadcrumbPosition && $(document).width() >= 980) {
        $('ol.breadcrumb').addClass('sticky').css({
            top: newPosition + "px"
        });
        $('div.hiddenDiv').css({
            height: "57px"
        });
    } else if (scroll > (breadcrumbPosition + $('.page-header').innerHeight()) && ($(document).width() < 980 && ($(document).width() > 550))) {
        $('ol.breadcrumb').addClass('sticky').css({
            top: "0px"
        });
        $('div.hiddenDiv').css({
            height: "57px"
        });

    } else if (scroll > (breadcrumbPosition + $('.page-header').innerHeight()) && ($(document).width() < 550)) {
        $('ol.breadcrumb').removeClass('sticky').animate('top', '0');
        $('div.hiddenDiv').css({
            height: "0px"
        });
    } else {
        $('ol.breadcrumb').removeClass('sticky').animate('top', '0');
        $('div.hiddenDiv').css({
            height: "0px"
        });
    }

    newPosition = $(document).height() - $('.page-content-wrapper').height() - 30;
};

$(window).on('scroll', breadcrumbScroll);

$(window).resize(function () {

    breadcrumbScroll();

    $(window).off('scroll', breadcrumbScroll);
    $(window).on('scroll', breadcrumbScroll);
});
