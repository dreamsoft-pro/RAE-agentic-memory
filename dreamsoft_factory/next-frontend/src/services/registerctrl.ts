javascript
import '@/lib/api';
// [BACKEND_ADVICE] Consider moving complex logic to backend services.

export default class RegisterCtrl {
    constructor($scope, $rootScope, $state, $filter, UserService, AuthService, Notification,
                CountriesService, RegisterWidget, LoginWidgetService, SocialWidgetService,
                SettingService, $cookieStore, vcRecaptchaService, MainWidgetService) {
        'ngInject';

        this.$scope = $scope;
        this.$rootScope = $rootScope;
        this.$state = $state;
        this.$filter = $filter;
        this.UserService = UserService;
        this.AuthService = AuthService;
        this.Notification = Notification;
        this.CountriesService = CountriesService;
        this.RegisterWidget = RegisterWidget;
        this.LoginWidgetService = LoginWidgetService;
        this.SocialWidgetService = SocialWidgetService;
        this.SettingService = SettingService;
        this.$cookieStore = $cookieStore;
        this.vcRecaptchaService = vcRecaptchaService;
        this.MainWidgetService = MainWidgetService;

        this.init();
    }

    init() {
        this.MainWidgetService.includeTemplateVariables(this.$scope, 'register');
        this.$scope.form = {};
        this.$scope.countries = [];
        this.$scope.onlyForCompanies = false;
        this.$scope._ = _;
        this.$scope.response = null;
        this.$scope.widgetId = null;
    }
}
