import api from '@/lib/api'; // Assuming this module wraps Axios

class ModuleValueService {
    private module: string;
    private resource: string; // Make sure to define these properties or pass them as parameters
    private cache: any; // You should replace 'any' with the actual type of your cache object
    private getAllDef?: Promise<void>; // Use optional chaining for promises

    async getAll(force = false): Promise<any> { // Return a promise instead of using _this.getAllDef.promise
        if (force || !this.cache.get(this.module)) {
            try {
                const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}${this.resource}`);
                this.cache.put(this.module, response.data);
                this.emit('ModuleValue.getAll', response.data); // Assuming you have a method to emit events
                return Promise.resolve(response.data);
            } catch (error) {
                console.error(error);
                return Promise.reject(error);
            }
        } else {
            return Promise.resolve(this.cache.get(this.module));
        }
    }

    getList(params: any): Promise<any> { // Assuming 'params' is needed for the request
        return this.getAll().then(data => data).catch(err => err); // Simplified promise handling
    }

    private emit(eventName: string, eventData: any) {
        // Implement your event emitting logic here
    }
}

export default ModuleValueService;