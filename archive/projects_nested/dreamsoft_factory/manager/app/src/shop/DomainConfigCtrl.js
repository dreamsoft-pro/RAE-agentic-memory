angular.module('digitalprint.app')
    .controller('shop.DomainConfigCtrl', function ($scope, $rootScope, $filter, $modal, DomainService, Notification) {

        $rootScope.$on('Domain:changeSuccess', function () {
            $scope.form = _.clone($rootScope.currentDomain, true);
        });
        $scope.form = _.clone($rootScope.currentDomain, true);


        $scope.save = function () {
            DomainService.editDomain($scope.form).then(function (data) {
                $rootScope.currentDomain = _.clone($scope.form);
                var idx = _.findIndex($rootScope.domains, {ID: $rootScope.currentDomain.ID});
                $rootScope.domains[idx] = _.clone($rootScope.currentDomain, true);
                Notification.success($filter('translate')('success'));
            }, function (data) {
                Notification.error($filter('translate')('error'));
            });
        };

    });