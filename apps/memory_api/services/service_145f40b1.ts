import api from '@/lib/api';

export default class PsConfigOption {

    private getResource(): string {
        // Implementation of this method is required.
        return '';
    }

    public fetchResource = async (resource: string): Promise<any> => {
        try {
            const response = await api.get($config.API_URL + resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    };

    public saveOperations = async (optID: number, controllerID: string, operations: any[]): Promise<any> => {
        const resource = this.getResource() + '/' + optID + '/optionOperations/' + controllerID;

        try {
            await api.patch($config.API_URL + resource, { operations });
            return 'Success';
        } catch (error) {
            throw error.response ? error.response : error;
        }
    };
}