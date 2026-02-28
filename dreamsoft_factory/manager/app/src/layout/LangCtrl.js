angular.module('digitalprint.app')
    .controller('layout.LangCtrl', function ($scope, $rootScope, $translate, $cookies, LangSettingsService) {

        $('.dropdown-toggle').dropdown();

        $rootScope.languages = {
            'en': {
                name: 'English',
                code: 'en'
            },
            'pl': {
                name: 'Polski',
                code: 'pl'
            }
        };

        $rootScope.activeLangs = [];

        LangSettingsService.getAll();
        $rootScope.$on('LangSettings.getAll', function (e, data) {
            $rootScope.languages = {};
            _.each(data, function (item) {
                $rootScope.languages[item.code] = item;
                if (item.active === 1) {
                    $rootScope.activeLangs.push(item);
                }
            });
        });

        $scope.switchLanguage = function (key) {

            if (_.isUndefined($rootScope.languages[key])) {
                key = 'en';
            }
            $translate.use(key);
            $rootScope.currentLang = $scope.currentLang = $rootScope.languages[key];
        };

        $scope.switchLanguage($translate.use());


    }).config(function ($translateProvider) {

    $translateProvider
        .fallbackLanguage(['en', 'pl'])
        .registerAvailableLanguageKeys(['en', 'pl'], {
            'en_US': 'en',
            'en_UK': 'en',
            'pl_PL': 'pl',
            'de_CH': 'de'
        })
        .useLoader('LangLoader');

    $translateProvider.determinePreferredLanguage();
});
