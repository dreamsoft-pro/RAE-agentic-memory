import { createDeferred } from '@/lib/utils'; // Assuming a utility to handle deferred objects
import api from '@/lib/api';

class CalcFileService {

    async deleteFile(typeID: number, fileID: string): Promise<void> {
        const resource = this.getUrl(typeID);
        const url = `${resource}/${fileID}`;

        try {
            await api.delete(url);
        } catch (error) {
            throw error;
        }
    }

    async getBySetID(setID: string | number): Promise<any> {
        const url = [process.env.NEXT_PUBLIC_API_URL, 'dp_products', setID, 'calcFilesUploaderSet'].join('/');

        try {
            return await api.get(url);
        } catch (error) {
            throw error;
        }
    }

    getUrl(typeID: number): string {
        // Implement the logic to get URL based on typeID
        return `some-url/${typeID}`;
    }
}