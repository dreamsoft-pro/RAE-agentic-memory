import api from '@/lib/api';
import { useState, useEffect } from 'react';

class OrderMessageService {
    private form: any;
    private order: any;

    constructor(form: any, order: any) {
        this.form = form;
        this.order = order;
    }

    async sendMessage() {
        const accessToken = await AuthDataService.getAccessToken();
        socket.emit('order.addMessage', {
            'orderID': this.order.ID,
            'message': this.form.message,
            'accessToken': accessToken,
            'companyID': this.getCompanyId()
        });
    }

    private getCompanyId(): string | number {
        // Implement the logic to retrieve company ID
        return '';  // Replace with actual implementation
    }
}

const useOrderMessages = (form: any, order: any) => {
    const [messageSent, setMessageSent] = useState(false);

    useEffect(() => {
        if (!messageSent && form.message) {
            new OrderMessageService(form, order).sendMessage().then(() => {
                setMessageSent(true);
                socket.on('order.messageSaved', (data: any) => {
                    if (data.ID !== undefined) {
                        if (form && data.isAdmin === 0) {
                            this.form.message = '';
                        }
                        getOrderMessages(order.ID);
                    }
                });
            });
        }
    }, [messageSent, form]);

    return null;
};