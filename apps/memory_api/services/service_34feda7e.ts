import api from '@/lib/api';

class OngoingService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async patchAdditionalOperation(data: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/additionalOperation/${data.ID}`, data);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async getAlreadyStartedTasks(ongoingID: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/alreadyStartedTasks/${ongoingID}`);
            return response.data;
        } catch (error) {
            return Promise.reject(error);
        }
    }
}