import axios from 'axios';
import { createDeferred } from './utils'; // Assuming you have a utility function to create deferred objects

class PhotoFolderService {
    static async getFacebookSharedFolder(folderId: string): Promise<any> {
        const [resolve, reject] = createDeferred();
        
        try {
            const response = await axios.get(`${url}folder/shared-by-facebook/${folderId}`, { headers });
            resolve(response.data);
        } catch (error) {
            reject(error.response ? error.response.status : 500);
        }

        return new Promise((resolve, reject) => {
            return [resolve, reject];
        }).promise;
    }

    static async getFacebookSharedPhoto(photoId: string): Promise<any> {
        const [resolve, reject] = createDeferred();
        
        try {
            const response = await axios.get(`${url}folder/image/shared-by-facebook/${photoId}`, { headers });
            resolve(response.data);
        } catch (error) {
            reject(error.response ? error.response.status : 500);
        }

        return new Promise((resolve, reject) => {
            return [resolve, reject];
        }).promise;
    }
}

// Utility function for deferred objects
export const createDeferred = () => {
    let resolveFn: (value?: any) => void;
    let rejectFn: (reason?: any) => void;

    const promise = new Promise((resolve, reject) => {
        resolveFn = resolve;
        rejectFn = reject;
    });

    return [resolveFn!, rejectFn!];
};