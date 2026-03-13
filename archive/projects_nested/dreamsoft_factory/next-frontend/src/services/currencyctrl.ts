javascript
// CurrencyCtrl.js

import '@/lib/api';
import UserService from './UserService';

export default class CurrencyController {
    constructor($scope, $rootScope, $cookieStore) {
        this.$scope = $scope;
        this.$rootScope = $rootScope;
        this.$cookieStore = $cookieStore;

        // [BACKEND_ADVICE] Handle currency switching logic
        this.switchCurrency = this.switchCurrency.bind(this);
    }

    switchCurrency(currency) {
        if (this.$rootScope.currentCurrency === currency) {
            return;
        }

        this.$rootScope.currentCurrency = currency;
        this.$cookieStore.put('currency', currency.code);

        // [BACKEND_ADVICE] Update user options with new currency
        if (this.$rootScope.logged) {
            UserService.editUserOptions(this.$rootScope.user.userID, {currency: currency.code}).then((savedData) => {
                console.log(savedData);
            });
        }

        this.$rootScope.$emit('Currency.changed', currency);
    }
}

angular.module('dpClient.app').controller('CurrencyCtrl', CurrencyController);
