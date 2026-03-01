import api from '@/lib/api';

class TypeService {
    private async checkMainCategory(categories: string[]): Promise<string[]> {
        const allTypes: string[] = [];
        
        if (categories.length > 0) {
            // Assuming 'checkMainCategory' is an API call or another function that needs to be implemented.
            const response = await api.get('/your-endpoint', { params: { categories } });
            return response.data.types; // Adjust the property based on your actual API response structure
        }
        
        return allTypes;
    }

    public async getAllTypes(categories: string[]): Promise<string[]> {
        const allTypes: string[] = [];

        if (categories.length > 0) {
            allTypes.push(...await this.checkMainCategory(categories));
        }

        return allTypes;
    }
}

export default TypeService;