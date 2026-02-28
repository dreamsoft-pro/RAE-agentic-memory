import api from '@/lib/api';

export default class HelpService {
    private resource: string = 'adminHelps';
    
    public async getQuestion(key: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${key}`);
            return response.data;
        } catch (error) {
            throw error.response || new Error('Unknown error');
        }
    }

    public getGroup(group: string): Promise<string> {
        // This part is commented out as it was in the original code.
        // You can uncomment and implement as needed:
        // return api.get(`${this.resource}/${group}`).then(response => response.data.plain(), err => Promise.reject(err));

        return Promise.resolve('getGroup');
    }
}