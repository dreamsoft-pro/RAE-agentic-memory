import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {

    static deletePhotoById(url: string, header: any, folderId: string, photoId: string): Promise<any> {
        return axios({
            url: `${url}folder/${folderId}/projectImage/${photoId}`,
            method: 'DELETE',
            headers: header,
            crossDomain: true
        }).then(response => response.data);
    }

    static getSharedByEmail(url: string, folderId: string, password: string): Promise<any> {
        return axios({
            url: `${url}folder/shared-by-mail/${folderId}`,
            method: 'POST',
            data: { password },
            crossDomain: true
        }).then(response => response.data).catch(error => { throw error.response.status; });
    }

    static getSharedByFacebook(url: string, folderId: string): Promise<any> {
        const def = new Promise((resolve, reject) => {
            axios({
                url: `${url}folder/shared-by-facebook/${folderId}`,
                method: 'GET',
                crossDomain: true
            }).then(response => resolve(response.data)).catch(error => reject(error.response.status));
        });
        return def;
    }
}