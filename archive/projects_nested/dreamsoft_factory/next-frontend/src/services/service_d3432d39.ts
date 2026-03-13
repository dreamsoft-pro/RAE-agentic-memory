import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static facebookShareFolder = async (_id: string, headers: Record<string, any>) => {
        try {
            const response = await axios.post(`${url}folder/facebook-share/${_id}`, {}, { headers, withCredentials: true });
            return response.status;
        } catch (error) {
            throw error.response ? error.response.status : 500;
        }
    };

    static facebookSharePhoto = async (_id: string, headers: Record<string, any>) => {
        try {
            const response = await axios.post(`${url}folder/image/facebook-share/${_id}`, {}, { headers, withCredentials: true });
            return response.status;
        } catch (error) {
            throw error.response ? error.response.status : 500;
        }
    };

}