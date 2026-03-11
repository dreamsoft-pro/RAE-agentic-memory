javascript
import '@/lib/api';
// [BACKEND_ADVICE] Move heavy logic to backend service

class ContactFormCtrl {
    constructor($scope, $state, $filter, Notification, SettingService, vcRecaptchaService) {
        this.$scope = $scope;
        this.$state = $state;
        this.$filter = $filter;
        this.Notification = Notification;
        this.SettingService = SettingService;
        this.vcRecaptchaService = vcRecaptchaService;

        const setting = new this.SettingService('additionalSettings');
        setting.getPublicSettings().then(settingsData => {
            if (settingsData.captchaPublicKey) {
                $scope.model = {
                    key: settingsData.captchaPublicKey.value
                };
            }
        });

        $scope.response = null;
        $scope.widgetId = null;

        this.init();
    }

    init() {
        // Initialization logic here
    }
}

angular.module('dpClient.app').controller('ContactFormCtrl', ContactFormCtrl);
