import api from '@/lib/api';

class DeviceService {
    private static async deleteResource(resource: string, id: number): Promise<any> {
        try {
            const response = await api.delete(`${resource}/${id}`);
            if (response.data.response) {
                // Simulate cache removal and resolve the promise with data
                console.log('Cache removed for collection');
                return response.data;
            } else {
                throw new Error('Data rejection occurred');
            }
        } catch (error) {
            throw error; // Re-throw error to be handled by the caller
        }
    }

    private static async getOngoings(deviceID: string): Promise<any> {
        try {
            const response = await api.get(`${resource}/${deviceID}/deviceOngoings`);
            return response.data;
        } catch (error) {
            throw error; // Re-throw error to be handled by the caller
        }
    }

    public static async deleteResourceWrapper(resource: string, id: number): Promise<any> {
        try {
            const data = await DeviceService.deleteResource(resource, id);
            return data;
        } catch (error) {
            throw new Error(error.message); // Handle error as needed or re-throw
        }
    }

    public static async getOngoingsWrapper(deviceID: string): Promise<any> {
        try {
            const data = await DeviceService.getOngoings(deviceID);
            return data;
        } catch (error) {
            throw new Error(error.message); // Handle error as needed or re-throw
        }
    }

    public static async ongoing(deviceID: string): Promise<void | any> {
        try {
            const data = await DeviceService.getOngoingsWrapper(deviceID);
            console.log('Got device ongoings:', data);
        } catch (error) {
            console.error('Failed to get device ongoings:', error.message);
        }
    }

    public static async deleteItem(resource: string, id: number): Promise<void | any> {
        try {
            const response = await DeviceService.deleteResourceWrapper(resource, id);
            console.log('Deleted resource with ID:', id);
        } catch (error) {
            console.error('Failed to delete resource:', error.message);
        }
    }
}

export default DeviceService;