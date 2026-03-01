
angular.module('digitalprint.app')
    .controller('contents.StyleEditCtrl', function ($scope, $rootScope, $filter, Notification, StyleService) {

        function  init() {

            $scope.file = {
                content: ''
            };

            StyleService.getMainFile().then(function (data) {
                $scope.file = data;
            });

        }

        $scope.save = function () {
            console.log(this.file.content);
            StyleService.saveMainFile(this.file.content).then( function(data) {
                if( data.response ) {
                    Notification.success($filter('translate')(data.info));
                } else {
                    Notification.error($filter('translate')(data.info));
                }
            }, function(error) {
                Notification.error($filter('translate')(error.info))
            });
        };

        init();

    });