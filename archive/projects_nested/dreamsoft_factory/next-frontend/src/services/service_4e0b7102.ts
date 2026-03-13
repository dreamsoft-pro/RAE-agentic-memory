import api from '@/lib/api';

export default class CategoryDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public setDescriptionFile(file: any): Promise<any> {
        return api.patch(`${this.resource}/files`, file)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }

    public getDescriptionFile(descID: string): Promise<any> {
        return api.get(`${this.resource}/descFiles/${descID}`)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }
}