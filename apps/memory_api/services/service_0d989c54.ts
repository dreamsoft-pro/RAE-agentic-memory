import axios, { AxiosResponse } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    private static url: string = 'your-api-url-here'; // Replace with your actual API URL
    private static header: Record<string, string> = {}; // Add headers if needed

    public static async getImageFolder(imageID: string): Promise<AxiosResponse<any>> {
        try {
            const response = await axios.get(`${PhotoFolderService.url}/imagefolderParent/${imageID}`, {
                headers: PhotoFolderService.header,
                crossDomain: true
            });
            return response;
        } catch (error) {
            throw new Error(`Failed to fetch image folder with ID ${imageID}: ${error}`);
        }
    }

    public static async getImageByAuthor(name: string): Promise<AxiosResponse<any>> {
        try {
            const response = await axios.get(`${PhotoFolderService.url}/get-image-by-autor/${name}`, {
                headers: PhotoFolderService.header,
                crossDomain: true
            });
            return response;
        } catch (error) {
            throw new Error(`Failed to fetch images by author ${name}: ${error}`);
        }
    }
}