import axios from 'axios';

class PhotoFolderService {
    static async setImagePlace(imageID: string, data: any, headers: any): Promise<void> {
        try {
            const response = await axios.post(`${url}/set-image-place/${imageID}`, data, {headers, withCredentials: true});
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : error.message;
        }
    }

    static async setImagePeoples(peoples: any[], imageID: string): Promise<void> {
        try {
            const response = await axios.post(`${url}/set-image-peoples/${imageID}`, {peoples}, {withCredentials: true});
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : error.message;
        }
    }
}