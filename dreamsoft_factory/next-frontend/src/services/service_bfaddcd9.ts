import api from '@/lib/api';

class ShiftService {
    private deviceResource: string;

    constructor(deviceResource: string) {
        this.deviceResource = deviceResource;
    }

    public updateModule(module: any): Promise<any> {
        return api.put(`${this.deviceResource}`, module)
            .then((response: any) => response.data)
            .catch((error: any) => { throw error; });
    }

    public removeFromDevice(id: string): Promise<void> {
        const url = `${this.deviceResource}/${id}`;
        return api.delete(url)
            .then(() => {})
            .catch((error: any) => { throw error; });
    }

    public sortOnDevice(sort: any): Promise<any> {
        const def = new Promise((resolve, reject) => {
            api.post(`${this.deviceResource}/sort`, sort)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });

        return def;
    }
}