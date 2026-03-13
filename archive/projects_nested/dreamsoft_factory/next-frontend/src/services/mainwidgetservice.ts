javascript
import { axiosInstance as api } from '@/lib/api';
import _ from 'lodash';

export const MainWidgetService = ($rootScope, $q, DpCategoryService, SettingService, PaymentService, $filter, $config) => {
    function getMegaMenu() {
        return new Promise((resolve, reject) => {
            DpCategoryService.getCategoryTree().then(categories => {
                if (_.size(categories) > 0) {
                    resolve(categories);
                } else {
                    reject(false);
                }
            });
        });
    }

    // [BACKEND_ADVICE] Add backend logic here
    function getCreditLimit() {
        return new Promise((resolve, reject) => {
            PaymentService.getCreditLimit().then(data => {
                resolve(data);
            }).catch(error => {
                reject(error);
            });
        });
    }

    // [BACKEND_ADVICE] Add backend logic here
    function getSkinName() {
        return new Promise((resolve, reject) => {
            SettingService.getSkinName().then(skinName => {
                resolve(skinName);
            }).catch(error => {
                reject(error);
            });
        });
    }

    return {
        getMegaMenu,
        getCreditLimit,
        getSkinName
    };
};
