import api from '@/lib/api';

class PauseService {
    private resource: string = 'yourResourceName'; // Define the resource here

    async sortResources(sort: any): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/sort`;
            
            const response = await api.patch(url, sort);
            return response.data;
        } catch (error) {
            throw error; // Ensure to handle the error appropriately
        }
    }

    // Add other methods here if needed

}

export default PauseService;

// Usage example:
const pauseServiceInstance = new PauseService();
pauseServiceInstance.sortResources({ /* sort data */ })
    .then(data => console.log('Sorted successfully:', data))
    .catch(error => console.error('Error sorting resources:', error));