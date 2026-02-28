import api from '@/lib/api';

export default class PsConfigAttributeService {
    private resource: string = 'ps_attributes';
    private cache: any;

    constructor() {
        this.cache = new Map();
    }

    async getAll(force?: boolean): Promise<any[]> {
        if (this.cache.has('collection') && !force) {
            return this.cache.get('collection');
        } else {
            try {
                const response = await api.get(this.resource);
                const data: any[] = response.data;
                this.cache.set('collection', data);
                return data;
            } catch (error) {
                throw error;
            }
        }
    }
}