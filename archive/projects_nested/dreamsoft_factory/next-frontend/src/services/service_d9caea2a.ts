import api from '@/lib/api';

class DpStatusService {
    private resource: string;
    private apiUrl: string;

    constructor(resource: string) {
        this.resource = resource;
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL; // Assuming you have an API URL defined in your Next.js environment variables
    }

    async remove(id: number): Promise<any> {
        try {
            const response = await api.delete(`${this.apiUrl}/${this.resource}/${id}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error; // You might want to handle the error differently based on your application requirements
        }
    }

    async sort(sort: string): Promise<any> {
        const def = Promise.defer(); // This is a placeholder, since there's no direct equivalent in TypeScript. We'll use plain promise directly.

        api.get(`${this.apiUrl}/${this.resource}?sort=${encodeURIComponent(sort)}`)
            .then((response) => {
                if (response.data.response) {
                    return def.resolve(response.data);
                } else {
                    return def.reject(response.data);
                }
            })
            .catch((error) => {
                return def.reject(error);
            });

        // Since we're using async/await, we need to change the implementation of sort to use await directly.
        try {
            const response = await api.get(`${this.apiUrl}/${this.resource}?sort=${encodeURIComponent(sort)}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error; // Similar to remove method, you might want to handle the error differently
        }

        return def.promise; // You won't need this line if you're using async/await directly as shown above.
    }
}

export default DpStatusService;