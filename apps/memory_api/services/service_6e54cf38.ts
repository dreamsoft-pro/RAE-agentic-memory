import axios, { AxiosResponse } from 'axios';

class PhotoFolderService {

    private static async copyPhoto(photoId: string, targetFolderId: string, headers: Record<string, any>): Promise<AxiosResponse> {
        return await axios.post(`${url}/folder/photo-copy/${photoId}`, {
            targetFolder: targetFolderId
        }, {
            headers,
            crossDomain: true,
            withCredentials: true
        });
    }

    static async createPhotobook(folder: any): Promise<void | never> {
        try {
            const response = await PhotoFolderService.copyPhoto('some-photo-id', 'some-target-folder-id', { someHeaderKey: 'someHeaderValue' });
            console.log(response.data);
        } catch (error) {
            if (axios.isAxiosError(error)) {
                console.error(`Request failed with status code ${error.response?.status}`);
            } else {
                console.error('An unexpected error occurred:', error);
            }
        }
    }
}