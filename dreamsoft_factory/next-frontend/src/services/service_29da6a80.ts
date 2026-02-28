import api from '@/lib/api';
import { useState, useEffect } from 'react';

class OrderMessages {
    private resource: any;
    private url: string | null = null;
    private scope: any;
    private order: any;
    private typeOfResource: string;

    constructor(scope: any, order: any, type: string) {
        this.scope = scope;
        this.order = order;
        this.typeOfResource = type;
    }

    async init() {
        try {
            const templateUrlResponse = await TemplateRootService.getTemplateUrl(103);
            this.url = templateUrlResponse.url;

            if (this.url) {
                this.resource = this.scope.$modal.open({
                    templateUrl: this.url,
                    scope: this.scope,
                    size: 'lg',
                    controllerAs: '$ctrl',
                    bindToController: true,
                    controller: class OrderMessagesController {
                        order = this.$scope.order;
                        messages = [];
                        typeOfResource = this.$scope.typeOfResource;

                        constructor($scope) {
                            this.$scope = $scope;
                            socket.emit('onOrder', { 'orderID': this.$scope.order.ID });

                            this.$scope.order.unreadMessages = 0;
                            getOrderMessages(this, this.$scope.order.ID);
                        }

                        send() {
                            // Implement send functionality
                        }
                    },
                });
            }
        } catch (error) {
            console.error('Failed to initialize order messages', error);
        }
    }
}

// Usage Example:
const scope = {}; // Assuming some context for the modal
const order = {}; // Some order object with ID property
const type = 'someType'; // Type of resource

const orderMessagesInstance = new OrderMessages(scope, order, type);
orderMessagesInstance.init();