import api from '@/lib/api';

class DpUserAddressService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async remove(data: any): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${data.ID}`;
        
        try {
            const response = await api.delete(url, { data });
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Failed to remove resource');
            }
        } catch (error) {
            throw error;
        }
    }
}

export default DpUserAddressService;