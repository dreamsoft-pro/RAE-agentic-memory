import api from '@/lib/api';

class ProcessService {
    static async deleteResource(resource: string, id: number): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, id].join("/")}`;
        
        try {
            const response = await api.delete(url);
            
            if (response.data.response) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static sort(sort: any): Promise<any> {
        return new Promise((resolve, reject) => {
            // Your sorting logic here
            // Example:
            const sortedData = /* your data sorting */;
            
            if (sortedData.success) {
                resolve(sortedData);
            } else {
                reject(sortedData.error || 'Sorting failed');
            }
        });
    }
}

export default ProcessService;