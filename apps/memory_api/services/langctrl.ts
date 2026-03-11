javascript
import '@/lib/api';
import _ from 'lodash';

angular.module('dpClient.app')
  .controller('LangCtrl', function ($scope, $rootScope, $translate, $cookieStore, $window, LangSettingsService,
                                   LangSettingsRootService, Notification, $langStorage) {

      $rootScope.$on('LangSettings.getAll', (e, data) => {
          const languages = {};
          _.each(data, item => {
              if(item.active === 1) {
                  languages[item.code] = item;
              }
          });
          $rootScope.languages = languages;
      });

      LangSettingsService.getAll();

      $scope.countLanguages = () => _.values($rootScope.languages).length;

      $scope.switchLanguage = key => $rootScope.$emit('changeLang', key);

      $scope.switchCurrency = currency => {
          const idx = _.findIndex($rootScope.currencies, {code: currency.code});
