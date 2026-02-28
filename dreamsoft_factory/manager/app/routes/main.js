angular.module('digitalprint.routes')
  .config(function($stateProvider, $locationProvider, $urlRouterProvider){

    var main = {};

    main.main = {
      name: 'main',
      abstract: true,
      templateUrl: 'views/main.html',
      controller: 'MainCtrl',
      ncyBreadcrumb: {
        skip: true
      }
    };

    main.base = {
      name: 'base',
      abstract: true,
      parent: 'main',
      resolve: {
        Domain: ['$q', 'DomainService', function($q, DomainService){
          var def = $q.defer();

          DomainService.getCurrentDomain().then(function(data){
            def.resolve(data);
          });

          return def.promise;
        }],
        AuthCheck: ['$q', '$rootScope', 'AuthService', function($q, $rootScope, AuthService) {
          var def = $q.defer();

          AuthService.check().then(function(data) {
            $rootScope.logged = true;
            def.resolve(data);
          }, function(data) {
            $rootScope.logged = false;
            def.resolve(data);
          });
          return def.promise;
        }],
        AdminMenu: ['$q', '$rootScope', '$http', '$config', function($q, $rootScope, $http, $config) {
          var def = $q.defer();

          $http({
            method: 'GET',
            url: $config.API_URL + 'adminmenu'
          }).success(function(data) {
            $rootScope.adminmenu = data;
            def.resolve(data);
          }).error(function(data) {
            def.reject(data);
          });

          return def.promise;
        }]
      },
      views: {
        '': {
          templateUrl: 'views/base.html'
        },
        'sidebar': {
          templateUrl: 'src/layout/templates/sidebar.html',
          controller: 'layout.SidebarCtrl'
        },
        'dropdown-user@base': {
          templateUrl: 'views/dropdown-user.html',
          controller: 'unauthorized.LoginCtrl'
        }
      },
      ncyBreadcrumb: {
        label: '{{langArr.home}}'
      }
    };

    main.unauthorized = {
      name: 'unauthorized',
      parent: 'main',
      abstract: true,
      templateUrl: 'views/unauthorized.html'
    };

    _.each(main, function(route){
      $stateProvider.state(route);
    });


    $urlRouterProvider.otherwise('/shop');

  });
