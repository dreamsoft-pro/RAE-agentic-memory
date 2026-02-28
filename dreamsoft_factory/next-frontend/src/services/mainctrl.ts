javascript
import { BACKEND_ADVICE } from '@/lib/api';
import MainWidgetService from '@/services/MainWidgetService';
import MenuTypesService from '@/services/MenuTypesService';

export default class MainCtrl {
    constructor($q, $scope, $rootScope, DpCartsDataService) {
        this.$q = $q;
        this.$scope = $scope;
        this.$rootScope = $rootScope;
        this.DpCartsDataService = DpCartsDataService;

        this.init();
    }

    async init() {
        await MainWidgetService.includeTemplateVariables(this.$scope, 'header');
        const megaMenu = await MainWidgetService.getMegaMenu();

        // [BACKEND_ADVICE] This logic should be considered for backend handling if it becomes complex.
        if (megaMenu.items.length > 0) {
            megaMenu.items[0].isVisible = true;
        }
        this.$rootScope.menuItems = megaMenu.items;

        if (megaMenu.visible === 1) {
            this.$rootScope.showMenu = true;
        } else {
            this.$rootScope.showMenu = false;
        }

        this.$rootScope.menuType = megaMenu.menuType || 1;

        this.$rootScope.allTypes = MenuTypesService.getAllTypes(megaMenu.items);
    }
}
