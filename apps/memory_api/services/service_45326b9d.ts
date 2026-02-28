import api from '@/lib/api';

export default class TypeDescriptionsService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    setDescriptionFile(file: any): Promise<any> {
        return api.patch(`${this.resource}/files`, file).then(
            (response: any) => response.data,
            (error: any) => Promise.reject(error)
        );
    }

    getDescriptionFile(descID: string): Promise<any> {
        return api.get(`${this.resource}/descFiles/${descID}`).then(
            (response: any) => response.data,
            (error: any) => Promise.reject(error)
        );
    }
}