import api from '@/lib/api';

class DeviceService {
    static moveOngoings(resource: string, deviceID: string, ongoingID: string, newDeviceID: string): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, deviceID, 'deviceOngoings', ongoingID, 'moveOngoings'].join("/")}`;
        
        return api.patch(url, { newDeviceID })
            .then(data => data.response ? Promise.resolve(data) : Promise.reject(data))
            .catch(error => Promise.reject(error));
    }

    static skills(deviceID: string): Promise<any> {
        const url = `${process.env.API_URL}/devices/${deviceID}/skills`;

        return api.get(url)
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}

export default DeviceService;