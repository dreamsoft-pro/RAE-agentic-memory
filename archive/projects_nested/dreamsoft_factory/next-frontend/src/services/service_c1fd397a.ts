import api from '@/lib/api';
import { useEffect } from 'react';

interface Notification {
    success(message: string): void;
    error(message: string): void;
}

interface $filter {
    translate(key: string): string;
}

interface OrderMessageService {
    sendEmailMessage(params: any): Promise<any>;
}

interface FormInterface {
    message: string;
    sendAlsoByEmail: boolean;
    [key: string]: any; // Allow for other potential keys in the form
}

export default function MyComponent({ socket, $scope, Notification, $filter, OrderMessageService, getMessages }: {
    socket: WebSocket | SocketIOClient.Socket;
    $scope: { form: FormInterface };
    Notification: Notification;
    $filter: $filter;
    OrderMessageService: OrderMessageService;
    getMessages: (scope: any, orderId: string) => void;
}) {
    useEffect(() => {
        if (!socket) return;

        socket.on('order.messageSaved', async function (data) {
            if (typeof data.ID !== 'undefined') {
                const resource = $scope.form; // Define before use
                const url = '/some/url'; // Placeholder, define actual URL or remove if not needed

                if (resource && data.isAdmin === 1) {
                    const params: { content?: string; orderID?: string; orderMessageID?: string } = {
                        content: data.content,
                        orderID: data.orderID,
                        orderMessageID: data.ID
                    };

                    try {
                        if (resource.sendAlsoByEmail) {
                            await OrderMessageService.sendEmailMessage(params);
                            Notification.success($filter('translate')('email_sended'));
                        }
                        
                        resource.message = '';
                        resource.sendAlsoByEmail = false;
                    } catch (errorData) {
                        Notification.error($filter('translate')(errorData.info));
                    }

                    getMessages($scope, 'order.ID'); // Ensure order.ID is defined or provide actual value
                }
            }
        });

        return () => {
            socket.off('order.messageSaved');
        };
    }, [socket]);
}