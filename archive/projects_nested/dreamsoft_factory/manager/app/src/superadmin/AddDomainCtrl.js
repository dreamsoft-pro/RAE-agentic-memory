angular.module('digitalprint.app')
    .controller('superadmin.AddDomainCtrl', function ($scope, $rootScope, DomainService, Notification) {

        $scope.form = {};

        $scope.saveDomain = function () {
            DomainService.addDomain($scope.form).then(function (data) {
                $scope.form = {};
                Notification.success("Ok");
                $rootScope.$emit('newDomainAdd')
            }, function (data) {
                console.log(data);
                Notification.error("Error");
            });

        }

    });
