angular.module('digitalprint.app')
    .controller('customerservice.RegisterCtrl', function ($scope, $filter, UserService, Notification, CountriesService) {

        $scope.form = {};
        $scope.countries = [];

        function init() {
            CountriesService.getAllEnabled().then(function(countriesData) {
                $scope.countries = countriesData;
            });
        }

        init();

        $scope.addUser = function () {

            UserService.add($scope.form).then(function (data) {
                $scope.form = {};
                Notification.success($filter('translate')('user_has_been_added'));
            }, function (data) {
                if( data.info ) {
                    var fullText = $filter('translate')(data.info);
                    if(data.afterInfo) {
                        fullText += ' - ' + data.afterInfo;
                    }
                    Notification.error(fullText);
                } else {
                    Notification.error($filter('translate')('unexpected_error'));
                }

            });

        }

    });