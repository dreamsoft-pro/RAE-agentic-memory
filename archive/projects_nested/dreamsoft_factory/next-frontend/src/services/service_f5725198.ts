import api from '@/lib/api';
import { useRef } from 'react';

class OrdersPanel {
    private socket: SocketIOClient.Socket;
    private offers: any[] = [];
    private userID: string;

    constructor(userID: string, socket: SocketIOClient.Socket) {
        this.userID = userID;
        this.socket = socket;
        this.init();
    }

    private init() {
        this.socket.emit('onOrdersPanel', { userID: this.userID });

        this.socket.on('order.newMessage', async (newMessage: any) => {
            const orderIdx = this.offers.findIndex((offer) => offer.ID === newMessage.orderID);
            if (orderIdx > -1) {
                if (!this.offers[orderIdx].unreadMessages) {
                    this.offers[orderIdx].unreadMessages = 1;
                } else {
                    this.offers[orderIdx].unreadMessages++;
                }
            }
        });
    }

    public doPayment(order: any): void {
        const templateUrl = await api.getTemplateUrl(72);
        // Assuming $modal is a custom modal service
        const modalInstance = $modal.open({
            templateUrl,
            backdrop: true,
            keyboard: false,
            size: 'lg',
            controller: ($scope, $modalInstance) => {
                // Define your modal logic here
            },
        });
    }
}