javascript
'use strict';

import { OffersService } from '@/lib/api';
import { BACKEND_ADVICE } from '@/constants'; // [BACKEND_ADVICE] for backend logic advice

const OffersCtrl = ($scope, $rootScope, $q, ClientZoneWidgetService, DpOrderService,
                    AddressService, $filter, DeliveryService, DeliveryWidgetService,
                    TemplateRootService, $modal, CommonService, $config,
                    AuthDataService, FileUploader, ProductFileService, Notification,
                    MainWidgetService, $timeout, PaymentService, AuthService, $state,
                    $stateParams) => {

    $scope.offers = [];
    $scope.offersCount = 0;

    $scope.pagingSettings = ClientZoneWidgetService.getPagingSettings();

    $scope.pageSizeSelect = ClientZoneWidgetService.getPageSizeSelect();
    
    // Fetch offers data from backend service
    OffersCtrl.fetchOffersData($scope);

    OffersCtrl.prototype.fetchOffersData = function ($scope) {
        OffersService.getOffers().then(response => {
            $scope.offers = response.data;
            $scope.offersCount = response.count;
        });
    };

};

export { OffersCtrl };
