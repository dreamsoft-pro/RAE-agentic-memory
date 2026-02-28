import api from '@/lib/api';

class MessagesService {
    private resource: string;

    constructor() {
        this.resource = 'messages'; // Define resource before use
    }

    public async getMessages(orderID: string): Promise<any[]> {
        const url = `/api/${this.resource}?order_id=${orderID}`; // Define url before use
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw new Error('Failed to fetch messages');
        }
    }

    public async displayMessages(scope: any, orderID: string): Promise<void> {
        try {
            const data = await this.getMessages(orderID);
            scope.messages = data; // Assuming scope is passed in from somewhere else
        } catch (error) {
            console.error(error);
        }
    }

    public getMessageModal() {
        return { messagesModal: 'messagesModal' }; // Return object as requested
    }
}

export default MessagesService;