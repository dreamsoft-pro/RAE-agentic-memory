import api from '@/lib/api';

class PsConfigAttributeTypeService {
    private resource: string = 'ps_attributetypes';
    private cache: { [key: string]: any } = {};

    constructor() {}

    async getAll(force?: boolean): Promise<any[]> {
        if (this.cache['collection'] && !force) {
            return this.cache['collection'];
        }

        try {
            const data = await api.get(this.resource);
            this.cache['collection'] = data.data.map(item => item.attributes); // Assuming data format
            return this.cache['collection'];
        } catch (error) {
            throw error;
        }
    }
}

export default PsConfigAttributeTypeService;