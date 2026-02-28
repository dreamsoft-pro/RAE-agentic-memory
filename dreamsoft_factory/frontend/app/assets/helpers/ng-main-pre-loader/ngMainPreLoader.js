/**
 * Created by Rafał on 11-07-2017.
 */
angular.module('dpClient.helpers')
    .directive('ngMainPreLoader', function ($config, $rootScope) {
        return {
            restrict: 'A',
            template: '<div ng-class="{finished:!showPreloader}" id="mainLoader">' +
                '<div class="main-pre-loader">' +
                '<span></span>' +
                '</div>' +
                '{{loadingCount}}' +
                '</div><span ng-if="errorCount" style="color:red; padding: 4px; position: fixed; right: 0;">errors: {{errorCount}}</span>',
            scope: {},
            controller: function ($scope, LoadingService, $timeout) {
                const TIMEOUT = 2000;
                let timer;
                let paused;
                $scope.showPreloader = 0;

                $scope.$on('loading:start', function (e, config) {
                    $scope.loadingCount = LoadingService.count()
                    if (!paused) {
                        $timeout.cancel(timer)
                        timer = $timeout(() => {
                            $scope.showPreloader = true
                        }, TIMEOUT/($scope.loadingCount>2 ? TIMEOUT : 1))
                    }

                });

                $scope.$on('loading:finish', function () {
                    $scope.loadingCount = LoadingService.count()
                    $scope.errorCount = LoadingService.errorCount()
                    if ($scope.loadingCount == 0) {
                        $timeout.cancel(timer)
                        $scope.showPreloader = false
                    }
                });

                $rootScope.$on('startPreLoader', function () {
                    $scope.showPreloader = true
                    paused = false
                });

                $rootScope.$on('stopPreLoader', function () {
                    $timeout.cancel(timer)
                    $scope.showPreloader = false
                    paused = true
                });
            }
        }
    });
