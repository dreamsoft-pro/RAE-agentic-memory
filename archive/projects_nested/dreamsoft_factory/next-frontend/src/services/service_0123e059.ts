import api from '@/lib/api';
import { useState, useEffect } from 'react';

export default class CopyProductModal {
    private scope: any;
    private product: any;
    private isVolumeChangeOnly: boolean = false;
    private isOrderAgain: boolean = false;
    private isEditOnly: boolean = false;

    constructor(scope: any, product: any, isVolumeChangeOnly?: boolean, isOrderAgain?: boolean, isEditOnly?: boolean) {
        this.scope = scope;
        this.product = product;
        this.isVolumeChangeOnly = isVolumeChangeOnly ?? false;
        this.isOrderAgain = isOrderAgain ?? false;
        this.isEditOnly = isEditOnly ?? false;

        this.loadTemplate();
    }

    private async loadTemplate() {
        try {
            const templateUrlResponse = await api.get('/api/template-url', { params: { id: 115 } });
            if (templateUrlResponse.data.url) {
                // Assuming $modal.open is a function provided by some modal service in your application
                this.openModal(templateUrlResponse.data.url);
            }
        } catch (error) {
            console.error('Error loading template URL:', error);
        }
    }

    private openModal(url: string): void {
        const stopSelectAttr = null;
        const stopSelect = null;

        // Assuming $modal is a service injected into your component
        this.scope.$modal.open({
            templateUrl: url,
            scope: this.scope,
            size: 'lg',
            controllerAs: '$ctrl',  // Optional, if you need to use controller-as syntax in the modal's controller
            controller: ['$scope', '$modalInstance', ($scope: any, $modalInstance: any) => {
                $scope.isVolumeChangeOnly = this.isVolumeChangeOnly;
                $scope.isOrderAgain = this.isOrderAgain;
                $scope.isEditOnly = this.isEditOnly;

                // Your modal controller logic here
            }]
        });
    }
}