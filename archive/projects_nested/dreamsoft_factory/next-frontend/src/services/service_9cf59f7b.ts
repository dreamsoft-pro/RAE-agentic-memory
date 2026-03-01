import api from '@/lib/api';

class OrderMessageService {

    private static async getCountAll(resource: string): Promise<number> {
        try {
            const response = await api.get(`${process.env.API_URL}/${resource}/countAll`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get count all for resource ${resource}: ${error}`);
        }
    }

    private static async sendEmailMessage(resource: string, data: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}/sendEmail`, data);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to send email message for resource ${resource}: ${error}`);
        }
    }

    public static async useService(resource: string, mode: 'getCountAll' | 'sendEmailMessage', payload?: any): Promise<any> {
        switch (mode) {
            case 'getCountAll':
                return await this.getCountAll(resource);
            case 'sendEmailMessage':
                if (!payload) throw new Error('Payload is required for sendEmailMessage');
                return await this.sendEmailMessage(resource, payload);
            default:
                throw new Error(`Unsupported mode: ${mode}`);
        }
    }

}

export default OrderMessageService;