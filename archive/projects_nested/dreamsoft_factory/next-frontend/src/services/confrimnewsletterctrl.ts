javascript
'use strict';

import { BackendApi } from '@/lib/api';
import Notification from './Notification';
import SettingService from './SettingService';

const module = angular.module('dpClient.app');

module.controller('index.ConfirmNewsletter', function ($rootScope, $scope, $state, $filter, Notification) {
    const setting = new SettingService('general');
    const backendApi = new BackendApi();

    $scope.confirmation = {};

    async function init() {
        console.log($state.params);
        try {
            const data = await setting.confirmNewsletter($state.params.token);
            if (data.response === true) {
                $scope.confirmation.success = data.info;
            } else {
                $scope.confirmation.error = data.info;
            }
        } catch (error) {
            Notification.error('Failed to confirm newsletter subscription.');
        }
    }

    init();
});
