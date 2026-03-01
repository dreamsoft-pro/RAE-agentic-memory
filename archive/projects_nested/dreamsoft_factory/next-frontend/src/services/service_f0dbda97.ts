import api from '@/lib/api';

class OngoingService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async patchOperatorAdditional(operator: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/operatorAdditional`, operator);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response did not have a valid format');
            }
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    public async showForItem(itemID: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/showForItem/${itemID}`);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

export default OngoingService;