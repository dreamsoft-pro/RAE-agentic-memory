import api from '@/lib/api';

class MyClass {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    public async fetchData(): Promise<void> {
        try {
            const response = await api.get(this.url);
            console.log('Fetched data:', response.data[this.resource]);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    }
}