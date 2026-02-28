javascript
import { BackendAPI } from '@/lib/api';
import { NotificationService } from '@/services/notification';
import { AuthDataService } from '@/services/auth-data';

export const OrderMessageWidgetService = (function() {
    function messagesModal(scope, order, socket, typeOfResource) {
        const modalInstance = $modal.open({
            templateUrl: 'src/orders/templates/modalboxes/order-messages.html',
            scope: scope,
            size: 'lg'
        });

        scope.typeOfResource = typeOfResource;
        scope.order = order;
        scope.messages = [];

        order.unreadMessages = 0;

        socket.emit('onOrder', {'orderID': order.ID});

        getMessages(scope, order.ID);

        scope.send = function() {
            // [BACKEND_ADVICE] Heavy logic should be handled in the backend
            BackendAPI.sendMessage(scope.message.text, order.ID)
                .then(response => {
                    if (response.success) {
                        NotificationService.success('Message sent successfully');
                    } else {
                        NotificationService.error('Failed to send message');
                    }
                })
                .catch(error => {
                    NotificationService.error('An error occurred while sending the message', error.message);
                });
        };
    }

    function getMessages(scope, orderId) {
        BackendAPI.getMessages(orderId)
            .then(messages => {
                scope.messages = messages;
            })
            .catch(error => {
                NotificationService.error('Failed to load messages', error.message);
            });
    }

    return {
        messagesModal: messagesModal
    };
})();
