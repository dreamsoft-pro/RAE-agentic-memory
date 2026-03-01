import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static async getImageByPlace(name: string): Promise<any> {
        try {
            const response = await axios.get(`${process.env.API_URL}/get-image-by-place/${name}`, {
                headers: process.env.API_HEADERS ? JSON.parse(process.env.API_HEADERS) : {}
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get image by place ${name}: ${error.response?.status}`);
        }
    }

    static async getImageByPeoples(name: string): Promise<any> {
        try {
            const response = await axios.get(`${process.env.API_URL}/get-image-by-peoples/${name}`, {
                headers: process.env.API_HEADERS ? JSON.parse(process.env.API_HEADERS) : {}
            });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get image by peoples ${name}: ${error.response?.status}`);
        }
    }
}