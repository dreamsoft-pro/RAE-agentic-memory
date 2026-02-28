import api from '@/lib/api';

class GroupDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    setDescriptionFile(file: any): Promise<any> {
        return api.patch(`${this.resource}/files`, file);
    }

    getDescriptionFile(descID: string): Promise<any> {
        return api.get(`${this.resource}/descFiles/${descID}`);
    }
}

export default GroupDescriptionsService;