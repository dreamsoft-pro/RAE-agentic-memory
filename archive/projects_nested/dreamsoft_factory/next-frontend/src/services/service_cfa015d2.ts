import api from '@/lib/api';

class MarginsService {
    private resource: string = 'margins_supplier';
    private url: string;

    constructor() {
        this.url = process.env.API_URL + '/' + this.resource;
    }

    async addSupplierMargins(data: any): Promise<any> {
        try {
            const response = await api.post(this.url, data);
            return response.data;
        } catch (error) {
            throw new Error('Failed to add supplier margins');
        }
    }

    async editSupplierMargins(id: string | number, data: any): Promise<any> {
        try {
            const response = await api.put(`${this.url}/${id}`, data);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to update supplier margin for ID ${id}`);
        }
    }

    async removeSupplierMargin(ID: string | number): Promise<void> {
        try {
            await api.delete(`${process.env.API_URL}/${this.resource}/${ID}`);
        } catch (error) {
            throw new Error(`Failed to delete supplier margin for ID ${ID}`);
        }
    }
}

export default MarginsService;