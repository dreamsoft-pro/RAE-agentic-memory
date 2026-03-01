import api from '@/lib/api';

export default class MailContentService {
    private resource: string = 'mail-content';
    private url: string;

    constructor() {
        this.url = `https://api.example.com/${this.resource}`;
    }

    public async getMailContents(): Promise<string[]> {
        try {
            const response = await api.get(this.url);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch mail contents', error);
            throw new Error('Unable to load mail content');
        }
    }

    public async addMailContent(newContent: string): Promise<void> {
        try {
            const response = await api.post(this.url, { content: newContent });
            console.log('New mail content added:', response.data);
        } catch (error) {
            console.error('Failed to add new mail content', error);
            throw new Error('Unable to add new mail content');
        }
    }

    public async deleteMailContent(id: string): Promise<void> {
        try {
            await api.delete(`${this.url}/${id}`);
            console.log(`Mail content with ID ${id} deleted`);
        } catch (error) {
            console.error(`Failed to delete mail content with ID ${id}`, error);
            throw new Error('Unable to delete specified mail content');
        }
    }
}