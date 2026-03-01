/**
 * Service: LangCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import * as angular from 'angular';
import { CookieStore } from 'ngcookie'; // Assuming ngcookie provides a CookieStore service
import { TranslateService } from '@ngx-translate/core'; // Adjust import based on your translation library
import _ from 'lodash';

// Define interfaces or types if necessary to type check the data and methods used in this module.
interface LangSettingsItem {
    active: number;
    code: string;
}

angular.module('dpClient.app')
  .controller('LangCtrl', ['ctx', '$rootScope', 'translate', 'cookieStore', '$window', 'LangSettingsService', 'LangSettingsRootService', 'Notification', '$langStorage', (ctx, $rootScope, translate: TranslateService, cookieStore: CookieStore, $window, LangSettingsService, LangSettingsRootService, Notification) => {
    // Initialize languages object to store active languages
    const languages = {};

    // Listen for language settings update event
    $rootScope.$on('LangSettings.getAll', function (e, data: LangSettingsItem[]) {
        _.each(data, (item: LangSettingsItem) => {
            if (item.active === 1) {
                languages[item.code] = item;
            }
        });
        $rootScope.languages = languages;
    });

    // Fetch all language settings
    LangSettingsService.getAll();

    // Function to count the number of available languages
    ctx.countLanguages = () => {
        return _.values($rootScope.languages).length;
    };

    // Function to switch language based on key
    ctx.switchLanguage = (key: string) => {
        $rootScope.$emit('changeLang', key);
    };

    // Function to switch currency and set it in cookie
    ctx.switchCurrency = (currency: { code: string }) => {
        const idx = _.findIndex($rootScope.currencies, { code: currency.code });
        if (idx !== -1) {
            $rootScope.currentCurrency = ctx.currentCurrency = $rootScope.currencies[idx];
            cookieStore.put('currency', $rootScope.currentCurrency[index].code);
        }
    };
}]);

// Configuration for translation setup
angular.module('dpClient.app').config(['$translateProvider', '$langStorageProvider', ($translateProvider, $langStorageProvider) => {
    const langArr = new Array($langStorageProvider.getLangCode());
    $translateProvider
        .fallbackLanguage(langArr)
        .registerAvailableLanguageKeys(langArr, {
            'pl_PL': 'pl',
            'en_US': 'en',
            'en_UK': 'en',
            'de_DE': 'de',
            'de_AT': 'de',
            'de_CH': 'de',
            'de_LI': 'de',
            'de_LU': 'de',
            'ru_RU': 'ru',
            'es_ES': 'es',
            'it_IT': 'it'
        })
        .useLoader('LangLoader')
        .preferredLanguage(langArr[0]);
}]);