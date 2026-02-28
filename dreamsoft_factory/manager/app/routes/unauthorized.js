angular.module('digitalprint.routes')
    .config(function ($stateProvider) {

        var unauthorized = {};

        unauthorized.login = {
            parent: 'unauthorized',
            name: 'login',
            url: '/login',
            views: {
                'content': {
                    templateUrl: 'src/unauthorized/templates/login.html',
                    controller: 'unauthorized.LoginCtrl'
                }
            },
            data: {
                bodyClass: 'login'
            }
        };

        _.each(unauthorized, function (route) {
            $stateProvider.state(route);
        });

    });