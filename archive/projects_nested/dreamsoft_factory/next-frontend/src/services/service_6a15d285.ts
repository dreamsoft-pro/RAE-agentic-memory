import api from "@/lib/api";

class ReclamationFaultService {

    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL; // Assuming environment variable for API URL is used.
    }

    public async postData<T>(resource: string, data: any): Promise<T> {
        try {
            const response = await api.post(this.apiUrl + resource, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error; // Rethrow the error to propagate it up.
        }
    }

    public async removeFault(faultID: string): Promise<void> {
        try {
            await api.delete(this.apiUrl + [resource, faultID].join('/')); // Ensure 'resource' is defined before use.
        } catch (error) {
            throw new Error('Failed to delete fault');
        }
    }

}

// Example usage of the class:
const service = new ReclamationFaultService();

service.postData('someResource', { /* your data */ })
    .then(data => console.log(data))
    .catch(error => console.error(error));

service.removeFault('12345')
    .then(() => console.log('Fault removed'))
    .catch(error => console.error(error));