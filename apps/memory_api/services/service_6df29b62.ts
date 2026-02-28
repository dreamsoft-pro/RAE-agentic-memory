import api from "@/lib/api";
import { DeviceService } from "./types"; // Assuming there are types defined in this file

class DeviceService {
    private resource: string = "devices";

    addService(deviceID: string, data: any): Promise<any> {
        return api.post(`${this.resource}/${deviceID}/deviceServices`, data)
            .then((response) => response.data)
            .catch((error) => Promise.reject(error));
    }

    deleteService(deviceID: string, id: string): Promise<void> {
        const url = `${this.resource}/${deviceID}/deviceServices/${id}`;
        return api.delete(url)
            .then(() => {})
            .catch((error) => Promise.reject(error));
    }
}

export default DeviceService;