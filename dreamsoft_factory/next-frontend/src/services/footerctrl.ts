javascript
import '@/lib/api';
// [BACKEND_ADVICE] Heavy logic should be handled in the backend service

export default class FooterCtrl {
    constructor(SettingService, NewsService, TextWidgetService) {
        this.sent = false;
        this.articles = [];
        this.showArticles = false;
        this.additionalSettings = {};

        this.Setting = new SettingService('general');
    }

    sendEmail() {
        this.Setting.setModule('general');
        if (this.newsletterAgreement === undefined || !this.newsletterAgreement) {
            Notification.warning($filter('translate')('subscription_to_newsletter_agreement_info'));
            return false;
        }
    }
}

FooterCtrl.$inject = ['SettingService', 'NewsService', 'TextWidgetService'];
angular.module('dpClient.app').controller('index.FooterCtrl', FooterCtrl);
