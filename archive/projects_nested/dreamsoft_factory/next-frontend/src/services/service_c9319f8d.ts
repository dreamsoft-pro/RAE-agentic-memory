import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static getProjectsForTypes(formats: string[]): Promise<any> {
        const url = '<your-api-url>'; // Replace with your actual URL
        const header = {}; // Add your headers here

        return axios.get(`${url}getProjectsForTypes`, {
            headers: header,
            params: { formats },
            crossDomain: true
        }).then(response => response.data)
          .catch(error => Promise.reject(error.response.status));
    }

    static getUrlImageByExtension(id: string, extension: string): string {
        return `${url}get-image-in-extension/${id}/${extension}`; // Replace url with your actual URL variable if needed
    }
}

export default PhotoFolderService;