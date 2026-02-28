import api from '@/lib/api';

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async addAdditionalOperation(operation: any): Promise<any> {
        try {
            const response = await api.post<[string, string]>([this.resource, 'additionalOperation'].join('/'), operation);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    public async patchOngoingAdditional(data: any): Promise<any> {
        try {
            const response = await api.patch<[string, string]>(`${process.env.API_URL}/${this.resource}/additional`, data);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

// Usage example:
const ongoingServiceInstance = new OngoingService('yourResourceName');
ongoingServiceInstance.addAdditionalOperation({ /* operation object */ })
    .then(data => console.log(data))
    .catch(error => console.error(error));

ongoingServiceInstance.patchOngoingAdditional({ /* data object */ })
    .then(data => console.log(data))
    .catch(error => console.error(error));