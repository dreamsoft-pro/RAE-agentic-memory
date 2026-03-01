import api from '@/lib/api';

class TemplateVariablesService {
    private resource: string;
    private id: number;

    constructor(resource: string, id: number) {
        this.resource = resource;
        this.id = id;
    }

    public deleteItem(): Promise<any> {
        const url = `${process.env.API_URL}/${this.resource}/${this.id}`;

        return api.delete(url).then((response) => response.data)
            .catch((error) => {
                throw error.response ? error : error.response;
            });
    }
}

export default TemplateVariablesService;