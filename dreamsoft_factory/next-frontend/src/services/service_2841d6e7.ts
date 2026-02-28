import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {
    static async setImageAutor(imageID: string, data: any, url: string, header: any): Promise<any> {
        try {
            const response = await axios.post(url + `set-image-autor/${imageID}`, data, { headers: header, withCredentials: true });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : error.message;
        }
    }

    static async setImagePlace(place: string, imageID: string): Promise<void> {
        const data = { place };
        // You would call `setImageAutor` here with the appropriate URL and header
        await this.setImageAutor(imageID, data, 'your-api-url-here', 'headers-object-here');
    }
}