import axios from 'axios';
import { Cache } from './cache'; // Assuming you have a cache implementation
import { Promise as BluebirdPromise } from 'bluebird';

const cache: Cache<any> = new Cache();

export class DomainService {
    static async getAll(force?: boolean): BluebirdPromise<any[]> {
        if (cache.get('collection') && !force) {
            return cache.get('collection');
        }

        try {
            const response = await axios.get(`${process.env.API_URL}/${resource}`);
            cache.set('collection', response.data);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    static editDomain(domain: any): BluebirdPromise<void> {
        const deferred = BluebirdPromise.defer();
        
        axios.post(`${process.env.API_URL}/domains`, domain)
            .then(response => {
                deferred.resolve(response.data);
            })
            .catch(error => {
                deferred.reject(error);
            });

        return deferred.promise;
    }
}