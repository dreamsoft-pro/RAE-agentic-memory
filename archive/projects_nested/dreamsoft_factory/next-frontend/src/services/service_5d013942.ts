import api from '@/lib/api';

export default class PsConfigAttributeNatureService {
    private resource: string = 'ps_attributenatures';
    private cache: { [key: string]: any } = {};

    constructor() {}

    public async getAll(force?: boolean): Promise<any[]> {
        if (this.cache['collection'] && !force) {
            return this.cache['collection'];
        }

        try {
            const data = await api.get(this.resource);
            this.cache['collection'] = data;
            return data;
        } catch (error) {
            throw error;
        }
    }
}