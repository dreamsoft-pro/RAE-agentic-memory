import axios from 'axios';
import { Cache } from './cache'; // Assuming you have a cache module

class ComplexService {
    private API_URL: string;
    private cache: Cache;

    constructor(API_URL: string, cache: Cache) {
        this.API_URL = API_URL;
        this.cache = cache;
    }

    async addGroup(complexID: number, name: string): Promise<any> {
        try {
            const response = await axios.post(
                `${this.API_URL}/${this.getResource()}/group/${complexID}`,
                { name }
            );
            if (response.data.response) {
                this.cache.remove(this.getResource());
                return response.data;
            } else {
                throw new Error('Failed to add group');
            }
        } catch (error) {
            throw error;
        }
    }

    editGroup(groupID: string, name: string): Promise<any> {
        const resource = this.getResource();
        return axios.post(
            `${this.API_URL}/${resource}/group/${groupID}`,
            { name }
        ).then(response => response.data)
          .catch(error => {
              throw error;
          });
    }

    private getResource(): string {
        // Implement your logic to get the resource
        return 'your-resource';
    }
}