import api from '@/lib/api';

class ShiftService {
    private resource: string;
    private url: string;

    constructor(resource: string) {
        this.resource = resource;
        this.url = `${process.env.API_URL}/${this.resource}`;
    }

    public create(data: any): Promise<any> {
        return api.post(this.url, data).then(response => response.data)
            .catch(error => { throw new Error(error.response ? error.response.data : error.message); });
    }

    public update(module: any): Promise<any> {
        return api.put(this.url, module).then(response => response.data)
            .catch(error => { throw new Error(error.response ? error.response.data : error.message); });
    }

    public remove(id: string): Promise<void> {
        const url = `${this.url}/${id}`;
        return api.delete(url).then(() => undefined)
            .catch(error => { throw new Error(error.response ? error.response.data : error.message); });
    }
}

export default ShiftService;