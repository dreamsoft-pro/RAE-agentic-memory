import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static async getImageByRating(min: number, max: number): Promise<any> {
        try {
            const response = await axios.post(`${process.env.API_URL}/get-image-by-rating`, { min, max }, {
                headers: process.env.HEADERS
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get image by rating: ${error.response ? error.response.status : 'Unknown'}`);
        }
    }

    static async setImageAuthor(author: string, imageID: number): Promise<void> {
        try {
            await axios.put(`${process.env.API_URL}/set-image-author/${imageID}`, { author }, {
                headers: process.env.HEADERS
            });
        } catch (error) {
            throw new Error(`Failed to set image author: ${error.response ? error.response.status : 'Unknown'}`);
        }
    }
}