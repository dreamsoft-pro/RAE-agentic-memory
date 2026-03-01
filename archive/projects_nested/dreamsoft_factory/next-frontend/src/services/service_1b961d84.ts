import { useState } from 'react';
import axios from 'axios';

class PhotoFolderService {
    static emailShare(email: string, folder: any): Promise<any> {
        const [domain, setLocation] = useState(window.location.protocol + '//' + window.location.hostname);
        if (window.location.port) {
            setLocation(domain + ':' + window.location.port);
        }

        return axios.post(`${url}folder/email-share/${folder._id}`, {
            email: email,
            host: domain,
            lang: localStorage.getItem('currentLang')?.code || ''
        }, {
            headers: header,
            withCredentials: true
        }).then(response => response.data)
          .catch(error => Promise.reject(error.response ? error.response.status : error));
    }

    static emailSharePhoto(email: string, photo: any): Promise<any> {
        return this.emailShare(email, photo);
    }
}