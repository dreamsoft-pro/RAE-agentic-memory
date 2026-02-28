javascript
import '@/lib/api';
import localStorageService from './services/localStorageService';
import SettingService from './services/settingService';

angular.module('dpClient.helpers')
    .directive('wcga', wcgaDirective);

function wcgaDirective() {
    return {
        restrict: 'E',
        scope: {},
        replace: true,
        templateUrl: 'src/index/templates/wcga.html',
        controller: WCGAController
    };

    // [BACKEND_ADVICE] Heavy logic should be handled in the backend or in a separate service.
}

WCGAController.$inject = ['$scope', 'localStorageService', 'SettingService'];

function WCGAController($scope, localStorageService, SettingService) {
    const setting = new SettingService('additionalSettings');

    setting.getPublicSettings().then(settingsData => {
        $scope.wcgaUsed = settingsData.wcgaUsed.value;
        if ($scope.wcgaUsed) {
            const lsKeys = localStorageService.keys();

            if (lsKeys.indexOf('wcgaKontrast') > -1) {
                $('body').addClass('wcga-contrast');
            }

            if (lsKeys.indexOf('wcgaFonts') > -1) {
                $('body').addClass('wcga-fonts');
            }
        }
    });
}
