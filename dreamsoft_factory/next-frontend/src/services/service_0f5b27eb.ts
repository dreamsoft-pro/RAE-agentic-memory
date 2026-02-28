import api from '@/lib/api';

export default class PsGroupService {
    private cacheResolve: any;

    constructor() {
        this.cacheResolve = new (window as any).CacheService('ps_groups');
    }

    async getAll(params: any, options?: any): Promise<any> {
        if (!params) {
            throw new Error("Params are required.");
        }
        
        options = options || {};

        try {
            const restangularPromise = api.all('ps_groups', params);
            const data = await this.cacheResolve.getList(restangularPromise, options);
            return data;
        } catch (error) {
            return Promise.reject(error);
        }
    }
}