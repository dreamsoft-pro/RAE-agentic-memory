import axios from 'axios';
import { CacheService as CacheServiceInterface } from './CacheService'; // Assuming there's an interface or type definition for CacheService

class CacheService implements CacheServiceInterface {
    private cache: any = {}; // Adjust the type based on your actual data structure
    private apiUrl: string;

    constructor(private config: { API_URL: string }) {
        this.apiUrl = config.API_URL;
    }

    private doRequest<T>(defer: Promise<any> | string, options: any, method?: 'getList' | 'get'): Promise<T> {
        const def = defer instanceof Promise ? defer : axios(this.getUrl(defer));
        
        return new Promise((resolve, reject) => {
            if (this.cache[defer]) {
                resolve(this.cache[defer]);
            } else if (def.then) {
                def.then(
                    data => {
                        this.cache[defer] = data;
                        options.onSuccess(defer, data);
                        resolve(data);
                    },
                    err => {
                        options.onError(err);
                        reject(err);
                    }
                );
            } else {
                axios.get(this.getUrl(defer))
                    .then(response => {
                        const data = response.data;
                        this.cache[defer] = data;
                        options.onSuccess(defer, data);
                        resolve(data);
                    })
                    .catch(error => {
                        options.onError(error);
                        reject(error);
                    });
            }
        });
    }

    private getUrl(defer: string): string {
        return `${this.apiUrl}${defer}`;
    }

    getList<T>(restangularPromise: Promise<any> | string, options: any): Promise<T> {
        return this.doRequest(restangularPromise, options, 'getList');
    }

    get<T>(restangularPromise: Promise<any> | string, options: any): Promise<T> {
        return this.doRequest(restangularPromise, options, 'get');
    }
}