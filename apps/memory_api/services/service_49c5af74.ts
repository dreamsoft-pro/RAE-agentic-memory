import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {
    static async saveFolderPosition(position: any, folder: any, url: string, header: any): Promise<any> {
        try {
            const response = await axios.post(`${url}folder/location/${folder._id}`, { location: position }, { headers: header });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : 500;
        }
    }

    static async savePosition(position: any, photo: any, url: string, header: any): Promise<any> {
        const def = axios.post(`${url}photo/location/${photo._id}`, { location: position }, { headers: header });
        return def.then(response => response.data).catch(error => {
            throw error.response ? error.response.status : 500;
        });
    }
}