import { useEffect, useState } from 'react';
import axios, { AxiosRequestConfig } from 'axios';

const apiUrlEditor = process.env.NEXT_PUBLIC_API_URL_EDITOR;
const accessTokenName = process.env.NEXT_PUBLIC_ACCESS_TOKEN_NAME;

class PhotoFolderService {
    private static instance: PhotoFolderService;
    private token: string | null;

    private constructor() {
        this.token = this.getAccessToken();
    }

    public static getInstance(): PhotoFolderService {
        if (!PhotoFolderService.instance) {
            PhotoFolderService.instance = new PhotoFolderService();
        }
        return PhotoFolderService.instance;
    }

    private getAccessToken(): string | null {
        const tokenCookie = document.cookie.split('; ').find(row => row.startsWith(`${accessTokenName}=`));
        return tokenCookie ? tokenCookie.split('=')[1] : null;
    }

    public movePhoto(data: any, fromFolderID: number, photo: any): Promise<void> {
        const config: AxiosRequestConfig = {
            method: 'POST',
            url: `${apiUrlEditor}/move-photo`,
            headers: {
                [accessTokenName]: this.token || '',
            },
            data,
        };
        return axios(config)
            .then(response => {
                // Handle success
                console.log('Photo moved successfully:', response.data);
            })
            .catch(error => {
                // Handle error
                console.error('Failed to move photo:', error.response?.data || error.message);
            });
    }
}

export default PhotoFolderService;