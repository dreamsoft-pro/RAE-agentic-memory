import api from '@/lib/api';

class PsGroupDescriptionService {
    private static async getAll(groupUrl: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/ps_groupDescriptions/groupDescriptionsPublic?groupUrl=${encodeURIComponent(groupUrl)}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    // Example of how to use the service
    static async fetchGroupDescriptions(groupUrl: string): Promise<any> {
        return PsGroupDescriptionService.getAll(groupUrl);
    }
}

export default PsGroupDescriptionService;

// Usage example (this would be in a component or another file)
import PsGroupDescriptionService from './path-to-service/PsGroupDescriptionService';

PsGroupDescriptionService.fetchGroupDescriptions('example-group-url')
    .then(data => console.log(data))
    .catch(error => console.error(error));