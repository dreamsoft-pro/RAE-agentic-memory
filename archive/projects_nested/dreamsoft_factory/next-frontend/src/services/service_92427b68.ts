import api from '@/lib/api';

class MarginsService {
    private resource: string;

    constructor() {
        this.resource = 'margins';
    }

    public async get(priceListID: number, natureID: number, groupID?: number, typeID?: number): Promise<any> {
        const params = [this.resource, priceListID, natureID];
        if (groupID) {
            params.push(groupID);
        }
        if (typeID) {
            params.push('');
            params.push(typeID);
        }

        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${params.join('/')}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching margins:', error);
            throw error; // Re-throw the error to be handled by a higher-level handler
        }
    }

    public async add(margin: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, margin);
            return response.data;
        } catch (error) {
            console.error('Error adding margins:', error);
            throw error; // Re-throw the error to be handled by a higher-level handler
        }
    }
}

export default MarginsService;