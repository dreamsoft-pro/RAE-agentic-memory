import api from '@/lib/api';

class DeviceService {

    private resource: string = 'devices'; // Example of defining resource

    public async deleteSpeed(speedID: number, deviceID: number): Promise<void> {
        try {
            const response = await api.delete(this.resource + '/' + deviceID + '/deviceSpeeds/' + speedID);
            return response;
        } catch (error) {
            throw error;
        }
    }

    public async getSpeedChanges(deviceID: number): Promise<any[]> {
        try {
            const response = await api.get(this.resource + '/' + deviceID + '/deviceSpeedChanges');
            return response.data; // Assuming the data is in a nested structure
        } catch (error) {
            throw error;
        }
    }

}

export default DeviceService;