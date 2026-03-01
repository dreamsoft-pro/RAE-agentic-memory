import api from '@/lib/api';

class LabelImpositionService {
    private readonly resource: string = 'labelImposition';
    private readonly url: string;

    constructor(private apiUrl: string) {
        this.url = `${apiUrl}/${this.resource}`;
    }

    public async getForType(typeID: number): Promise<any> {
        try {
            const response = await api.get(`${this.url}/${typeID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default LabelImpositionService;