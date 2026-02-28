import axios, { AxiosResponse } from 'axios';
import { Cache } from './cache'; // Assuming cache module exists

export class ComplexService {
    private API_URL: string;
    private cache: Cache;

    constructor(API_URL: string, cache: Cache) {
        this.API_URL = API_URL;
        this.cache = cache;
    }

    public async postItem(baseID: number, typeID: number, complexGroupID: number): Promise<any> {
        try {
            const response: AxiosResponse = await axios.post(`${this.API_URL}/resource`, {
                baseID,
                typeID,
                complexGroupID
            });

            if (response.data.ID) {
                this.cache.remove('resource'); // Adjust 'resource' to actual resource key
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public edit(item: any): Promise<any> {
        const defer = this.promiseConstructor();
        axios.post(`${this.API_URL}/resource`, item)
            .then((response: AxiosResponse) => {
                if (response.data.ID) {
                    this.cache.remove('resource'); // Adjust 'resource' to actual resource key
                    defer.resolve(response.data);
                } else {
                    defer.reject(response.data);
                }
            })
            .catch((error) => {
                defer.reject(error.response ? error.response.data : error.message);
            });

        return defer.promise;
    }

    private promiseConstructor() {
        const resolve: (value?: any) => void = () => {};
        const reject: (reason?: any) => void = () => {};

        const promise = new Promise((res, rej) => {
            resolve = res;
            reject = rej;
        });

        return { resolve, reject, promise };
    }
}