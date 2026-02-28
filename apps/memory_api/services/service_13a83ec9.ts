import api from '@/lib/api';

class SubcategoryDescriptionsService {
    public removeDescriptionFile(fileID: string): Promise<void> {
        const resource = 'subcategories'; // Define resource before use

        return api.delete(`${resource}/files/${fileID}`)
            .then((data) => {
                return data;
            })
            .catch((error) => {
                throw error;
            });
    }
}

export default SubcategoryDescriptionsService;