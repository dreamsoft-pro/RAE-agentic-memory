import api from '@/lib/api';

class PsConfigAttributeService {
    private resource: string = 'path_to_resource'; // Define your resource path

    public getOne(attrID: number): Promise<any> {
        return new Promise((resolve, reject) => {
            api.get(this.resource + '/' + attrID)
                .then(response => {
                    if (response.data.ID) {
                        resolve(response.data);
                    } else {
                        reject(response.data);
                    }
                })
                .catch(error => {
                    reject(error.response ? error.response.data : error.message);
                });
        });
    }

    public add(item: any): Promise<any> {
        return new Promise((resolve, reject) => {
            api.post(this.resource, item)
                .then(response => {
                    if (response.data.ID) {
                        // Assuming cache.remove is a function you have defined elsewhere
                        this.cacheRemove('collection');
                        resolve(response.data);
                    } else {
                        reject(response.data);
                    }
                })
                .catch(error => {
                    reject(error.response ? error.response.data : error.message);
                });
        });
    }

    private cacheRemove(key: string): void {
        // Implement your caching mechanism here
    }
}

export default PsConfigAttributeService;