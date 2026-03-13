angular.module('dpClient.config', []);
angular.module('dpClient.routes', ['ui.router', 'restangular']);
angular.module('dpClient.directives', []);
angular.module('digitalprint.services', ['LocalStorageModule']);
angular.module('dpClient.helpers', ['ui-notification']);
angular.module('dpClient.filters', []);


angular.module('dpClient.app', [
    'LocalStorageModule',
    'ui.bootstrap',
    'pascalprecht.translate',
    'ngCookies',
    'ngAnimate',
    'angular-api-collection',
    'ui.sortable',
    'ncy-angular-breadcrumb',
    'ngSanitize',
    'textAngular',
    'btford.socket-io',
    'angularFileUpload',
    'jkuri.gallery',
    'angular-carousel',
    'dpClient.routes',
    'dpClient.directives',
    'digitalprint.services',
    'dpClient.helpers',
    'dpClient.filters',
    'dpClient.config',
    'bw.paging',
    'wt.responsive',
    'ngScrollbars',
    'rzModule',
    'vcRecaptcha',
    'updateMeta',
    'ngMockE2E'
])
    .config(function ($configProvider, $locationProvider, $urlRouterProvider, $stateProvider, RestangularProvider,
                      localStorageServiceProvider, ApiCollectionProvider, $breadcrumbProvider, $httpProvider, $provide) {

        $configProvider.set('API_URL', 'http://localtest.me/api/');
        $configProvider.set('API_URL_EDITOR', 'http://localhost:1351/api/');
        RestangularProvider.setBaseUrl('http://localtest.me/api/');
        $configProvider.set('AUTH_URL', 'http://localtest.me:2600/');
        $configProvider.set('STATIC_URL', 'http://localtest.me/static/');
        $configProvider.set('SOCKET_URL', 'http://localtest.me:2600');
        $configProvider.set('EDITOR_URL', 'http://localhost:1400');

        function $LangStorageProvider() {
            return {
                $get: function () {
                    return this
                },
                getLangCode: () => 'pl'
            }
        }
        $provide.provider('$langStorage',$LangStorageProvider);
        $locationProvider.html5Mode(true);
        $urlRouterProvider.deferIntercept();

        $urlRouterProvider.otherwise(function ($injector, $location) {
            return '/deliveries';
        });

        RestangularProvider.setMethodOverriders(['put', 'patch']);

        localStorageServiceProvider.setPrefix('digitalprint');


        $httpProvider.interceptors.push('httpMethodOverride');
        $httpProvider.interceptors.push('loadingInterceptor');
        $httpProvider.interceptors.push('responseErrorInterceptor');

    })
    .run(function ($q, $rootScope, $config, $state, $cookieStore, routes, getDomains, $location, Notification,
                   $filter, $timeout, $urlRouter, $stateParams, AuthDataService, $window, translateRouting, LangService,
                   DpOrderService, $httpBackend) {
        $httpBackend.whenGET(new RegExp('api\/lang\/')).respond(200, {});
        $httpBackend.whenGET(/domains/).respond(200, [{}]);
        $httpBackend.whenGET(new RegExp('api\/routes\/translateState')).respond(200, [{}]);
        $httpBackend.whenGET(new RegExp('api\/langsettings')).respond(200, [{}]);
        $httpBackend.whenGET(/\.html$/).passThrough();

        $rootScope.currentCurrency={code:'PLN'}

        $urlRouter.sync();
        $urlRouter.listen();
        $rootScope.routes=[]
        $rootScope.$state = $state;
        $rootScope.defaultLangCode='pl'
        translateRouting.request($state.current.name, $stateParams, 'pl').then( function( data ) {

        });
        $configProviderRef = $config;

        /*$rootScope.$on('$stateChangeStart', function (event, toState, toParams, fromState, fromParams) {
            console.log(toState)
        });*/

        /*$rootScope.$on('cartRequired', function (e,is) {//TODO
            DpOrderService.getCart().then(function(data){
                $rootScope.carts=data.carts;
                $rootScope.productCount=data.order && data.order.products ? data.order.products.length : 0;
            })
        });*/

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

    .factory('loadingInterceptor', function ($q, $rootScope, LoadingService) {
        return {
            request: function (config) {
                LoadingService.requested();
                config.requestTimestamp = new Date().getTime();
                $rootScope.$broadcast('loading:start');
                return config;
            },
            response: function (response) {
                LoadingService.responsed();
                $rootScope.$broadcast('loading:finish');
                return response;
            },
            responseError: function (rejection) {

                if (rejection.status == 401) {
                    LoadingService.responsed();
                } else {
                    LoadingService.countError();
                }

                $rootScope.$broadcast('loading:finish');
                return $q.reject(rejection);
            }
        }
    })
    .factory('responseErrorInterceptor', function ($q, $injector, $timeout) {
        return {
            responseError: function (response) {
                console.log('responseError Status: ' + response.status);

                if (response.status == 0 || response.status == 408 || response.status > 500) {
                    var $http = $injector.get('$http');
                    return $timeout(function () {
                        return $http(response.config);
                    }, 3000, false);
                } else {
                    return $q.reject(response);
                }

            }
        }
    })
    .factory('routes', function ($http, $config, $q, $rootScope, $cookieStore) {
        return {
            getAll: function () {

                var def = $q.defer();

                $http({
                    url: $config.API_URL + ['routes', 'show'].join('/'),
                    method: 'GET'
                }).then(function successCallback(response) {
                    def.resolve(response);
                }, function errorCallback(response) {
                    def.reject(response);
                });
                return def.promise;
            },
            setAll: function () {
                var def = $q.defer();

                var defaultLang = $cookieStore.get('lang') ? $cookieStore.get('lang') : getLangCode();

                var actDate = new Date();
                var dateStr = actDate.getHours() + actDate.getMinutes() + actDate.getSeconds();

                var state;

                var counter = 0;
                //this.getAll().then(function (res) {

                _.each($rootScope.routes, function (value, index) {

                    if (value.abstract == 1) {
                        value.abstract = true;
                    } else {
                        value.abstract = false;
                    }

                    if (value.langs && angular.isDefined(value.langs[defaultLang]) && value.langs[defaultLang].url != null) {

                        state = {
                            "name": value.name,
                            "url": value.langs[defaultLang].url,
                            "parent": value.parent,
                            "abstract": value.abstract,
                            "views": {},
                            "ncyBreadcrumb": {
                                "label": value.langs[defaultLang].name
                            }
                        };
                    } else {

                        state = {
                            "name": value.name,
                            "parent": value.parent,
                            "abstract": value.abstract,
                            "views": {},
                            "ncyBreadcrumb": {
                                "skip": true
                            }
                        };

                    }

                    if (angular.isDefined(value.controller) && value.controller != null) {
                        state.controller = value.controller;
                    }

                    if (value.abstract === true && value.name == 'main') {
                        var actTemplate = value.views.pop();

                        state.templateUrl = actTemplate.template.url + '?ver=' + dateStr;

                        delete state.views;

                    } else if (value.route === true) {

                        delete state.views;

                    } else {

                        angular.forEach(value.views, function (view) {

                            if (view.template) {

                                //$templateCache.get()

                                console.log( view.template );

                                state.views[view.name] = {
                                    templateUrl: view.template.url + '?ver=' + dateStr,
                                    controller: view.controller
                                };
                            }

                        });

                    }

                    $stateProviderRef.state(value.name, state);

                    counter++;
                    if (counter == res.data.length) {
                        def.resolve(true);
                    }

                });
                //});

                return def.promise;
            },
            findOne: function (name) {
                var def = $q.defer();

                _.each($rootScope.routes, function (each) {
                    if (each.name === name) {
                        def.resolve(each);
                    }
                });

                return def.promise;
            }
        };
    })
    .factory('getDomains', function ($q, $http, $config) {
        return {
            request: function () {

                var def = $q.defer();

                $http({
                    url: $config.API_URL + ['domains'].join('/'),
                    method: 'GET'
                }).then(function (res) {
                    def.resolve(res.data)
                }, function (err) {
                    def.reject(new Error(err));
                });

                return def.promise;
            }
        };
    })
    .factory('translateRouting', function ($q, $rootScope, $http, $config) {
        return {
            request: function (actualState, stateParams, lang) {

                var def = $q.defer();
                var params=stateParams;
                params.lang=lang;
                $http({
                    url: $config.API_URL + ['routes', 'translateState', actualState].join('/'),
                    method: 'GET',
                    params: params
                }).then(function (res) {
                    def.resolve(res.data)
                }, function (err) {
                    def.reject(new Error(err));
                });

                return def.promise;
            }
        };
    })


angular.module('dpClient.helpers').directive('initBind', function ($compile) {
    return {
        restrict: 'A',
        link : function (scope, element, attr) {
            attr.$observe('ngBindHtml',function(){
                if(attr.ngBindHtml){
                    $compile(element[0].children)(scope);
                }
            })
        }
    };
});

