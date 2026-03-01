javascript
import { BackendAdvice } from '@/lib/api';
import LoadingService from './LoadingService';

const ngMainPreLoaderDirective = ($config, $rootScope) => {
    return {
        restrict: 'A',
        template: `<div ng-class="{finished:!showPreloader}" id="mainLoader">
                    <div class="main-pre-loader">
                        <span></span>
                    </div>
                    {{loadingCount}}
                </div><span ng-if="errorCount" style="color:red; padding: 4px; position: fixed; right: 0;">errors: {{errorCount}}</span>`,
        scope: {},
        controller: function ($scope) {
            const TIMEOUT = 2000;
            let timer;
            let paused = false;
            $scope.showPreloader = true;

            // [BACKEND_ADVICE] Handle loading logic
            $scope.$on('loadingStart', (event, data) => {
                if (!paused) {
                    $scope.loadingCount++;
                    $scope.errorCount += data.errors || 0;
                }
            });

            $scope.$on('loadingFinish', () => {
                paused = true;
                timer = setTimeout(() => {
                    $scope.showPreloader = false;
                    $scope.$apply();
                }, TIMEOUT);
            });
        },
    };
};

export default ngMainPreLoaderDirective;

// Register directive in module
import angular from 'angular';
const dpClientHelpersModule = angular.module('dpClient.helpers', []);
dpClientHelpersModule.directive('ngMainPreLoader', ngMainPreLoaderDirective);

