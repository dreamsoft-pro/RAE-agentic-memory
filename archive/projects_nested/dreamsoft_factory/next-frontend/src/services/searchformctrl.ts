javascript
// SearchFormCtrl.js
import { searchService } from '@/lib/api';
import { Notification } from 'angular-components';

export default class SearchFormCtrl {
    constructor($scope, $state, $filter) {
        this.$scope = $scope;
        this.$state = $state;
        this.$filter = $filter;

        // Initialize searchText if needed
        this.searchText = '';
    }

    search() {
        /**
         * @param this object
         * @param this.searchText string
         */
        if (this.searchText.length < 3) {
            Notification.warning(this.$filter('translate')('enter_minimum_chars').replace("%d", 3));
            return;
        }
        
        // [BACKEND_ADVICE] Consider moving complex logic to searchService
        this.$state.go('search', { text: this.searchText });
    }
}

SearchFormCtrl.$inject = ['$scope', '$state', '$filter'];
