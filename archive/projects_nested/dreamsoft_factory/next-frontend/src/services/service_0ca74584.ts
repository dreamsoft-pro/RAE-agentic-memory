import api from '@/lib/api';

class MetaTagService {
    static async edit(metaTag: any, images: any[], resource?: string): Promise<any> {
        if (resource === undefined) {
            resource = 'dp_mainMetaTags';
        }
        
        console.log(metaTag);
        
        try {
            const response = await api.put(`${resource}/${metaTag.ID}`, {
                languages: metaTag.languages,
                routeID: metaTag.routeID,
                ID: metaTag.ID
            });
            
            return response.data;
        } catch (error) {
            throw error;  // Handle or log the error as necessary.
        }
    }

    static async deleteImage(lang: string, imageID: number, resource?: string): Promise<void> {
        if (resource === undefined) {
            resource = 'dp_mainMetaTags';
        }

        console.log('something is working');
        
        try {
            // Assuming there's a method on the api object for deleting images.
            await api.delete(`${resource}/images/${lang}/${imageID}`);
        } catch (error) {
            throw error;  // Handle or log the error as necessary.
        }
    }
}