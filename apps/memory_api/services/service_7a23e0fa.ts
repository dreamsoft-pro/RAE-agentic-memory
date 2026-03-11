import api from '@/lib/api';

export default class DpUserAddressService {
    private userID: string;
    private resource: string;

    constructor(userID: string) {
        this.userID = userID;
        this.resource = ['users', this.userID, 'address'].join('/');
    }

    public async getAllAddresses(): Promise<any> {
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}?type=1`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getAllAddressesVat(): Promise<any> {
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}?type=2`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}