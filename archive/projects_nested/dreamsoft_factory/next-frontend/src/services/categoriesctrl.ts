javascript
'use strict';

import { BackendApi } from '@/lib/api';
import { Notification } from '@imports/notification';
import { SubCategoryDescriptionService } from '@services/sub-category-description.service';
import { MainWidgetService } from '@services/main-widget.service';

const categoriesCtrl = {
    bindings: {},
    controllerAs: 'categoriesCtrl',
    controller: class CategoriesController {
        constructor($scope, $q, $rootScope, $filter, DpCategoryService, $stateParams) {
            this.$scope = $scope;
            this.$q = $q;
            this.$rootScope = $rootScope;
            this.$filter = $filter;
            this.DpCategoryService = DpCategoryService;
            this.$stateParams = $stateParams;
            this.SubCategoryDescriptionService = SubCategoryDescriptionService;
            this.MainWidgetService = MainWidgetService;

            this.descriptions = [];
            this.galleries = [];
            this.subCategories = [];

            this.init();
        }

        init() {
            this.items = [];
            this.form = {};
            this.groups = [];
            this.category = {};

            const currentCategoryUrl = this.currentCategoryUrl = this.$stateParams.categoryurl;
            this.getContains(currentCategoryUrl);
            BackendApi.getOne(currentCategoryUrl).then(cat => {
                this.getDescription(currentCategoryUrl);
                this.MainWidgetService.includeTemplateVariables(this.$scope, 'category', undefined, undefined, cat.ID);
            });
        }

        getContains(categoryUrl) {
            // [BACKEND_ADVICE] Add backend logic here
        }

        getDescription(categoryUrl) {
            // [BACKEND_ADVICE] Add backend logic here
        }
    },
};

export { categoriesCtrl };
