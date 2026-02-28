import { AxiosPromise, AxiosRequestConfig } from 'axios';
import axios from 'axios';

class ComplexService {
    private API_URL: string;

    constructor(API_URL: string) {
        this.API_URL = API_URL;
    }

    private getResource(): string {
        // Implement the logic to get resource here
        return '';
    }

    public updateGroup(groupID: number, name: string): Promise<any> {
        const url = `${this.API_URL}/${[this.getResource(), 'group'].join('/')}`;

        axios.put(url, { ID: groupID, name }).then((response) => {
            if (response.data.response) {
                this.cacheRemove(this.getResource());
                response.config.promise.resolve(response.data);
            } else {
                response.config.promise.reject(response.data);
            }
        }).catch((error) => {
            error.config?.promise.reject(error);
        });

        const promise = new Promise<any>((resolve, reject) => {
            return { resolve, reject };
        });

        return promise;
    }

    private cacheRemove(resource: string): void {
        // Implement the logic to remove from cache here
    }

    public relatedFormat(baseFormatID: number): Promise<any> {
        const resource = this.getResource();
        const def = new Promise((resolve, reject) => {
            axios.get(`${this.API_URL}/${resource}`).then(response => {
                resolve(response.data);
            }).catch(error => {
                reject(error);
            });
        });

        return def;
    }
}