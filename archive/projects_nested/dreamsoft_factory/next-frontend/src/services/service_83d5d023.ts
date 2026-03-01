import api from '@/lib/api';

OperationService.deleteItem = async function(resource: string, id: number): Promise<any> {
    const url = `${process.env.API_URL}/${[resource, id].join("/")}`;
    try {
        const response = await api.delete(url);
        if (response.data.response) {
            cache.remove('collection');
            return response.data;
        } else {
            throw new Error('Failed to delete item');
        }
    } catch (error) {
        throw error;
    }
};

OperationService.sort = async function(sort: any): Promise<any> {
    try {
        // Your logic for sorting goes here
        const data = await api.get(`${process.env.API_URL}/some-endpoint`, { params: { sort } });
        return data.data; // Assuming the API returns a response object with data inside it.
    } catch (error) {
        throw error;
    }
};