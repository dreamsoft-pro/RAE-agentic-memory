import api from '@/lib/api';

class PsWorkspaceService {
    private cache: any;

    constructor() {
        this.cache = {};
    }

    async getAll(force?: boolean): Promise<any[]> {
        if (this.cache['collection'] && !force) {
            return this.cache['collection'];
        } else {
            try {
                const response = await api.get('ps_workspaces');
                const collection: any[] = response.data;
                this.cache['collection'] = collection;

                if (force) {
                    // Assuming $rootScope.$emit is a custom event emitter in the context of Next.js
                    // For simplicity, we'll use console.log to simulate this behavior.
                    console.log('ps_workspaces', collection);
                }

                return collection;
            } catch (error) {
                throw error;
            }
        }
    }
}

export default PsWorkspaceService;