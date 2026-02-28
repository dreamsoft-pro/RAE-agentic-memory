import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static async findPhoto(name: string): Promise<any> {
        try {
            const response = await axios.post(`${process.env.API_URL}/folder/findImage/${name}`, {}, {
                headers: JSON.parse(process.env.API_HEADERS || '{}'),
                withCredentials: true,
                crossDomain: true
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to find photo: ${error.response?.status}`);
        }
    }

    static async voteFolder(folderId: string, vote: number): Promise<any> {
        try {
            const response = await axios.post(`${process.env.API_URL}/folder/${folderId}/vote`, { vote }, {
                headers: JSON.parse(process.env.API_HEADERS || '{}'),
                withCredentials: true,
                crossDomain: true
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to vote for folder: ${error.response?.status}`);
        }
    }

}