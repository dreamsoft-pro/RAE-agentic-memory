import { useEffect, useState } from 'react';
import axios from 'axios';

class PhotoFolderService {
    static async getPhotoSharedByEmail(photoId: string, password: string): Promise<any> {
        try {
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/folder/image/shared-by-mail/${photoId}`, { password }, { crossDomain: true });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get photo shared by email. Status code: ${error.response?.status}`);
        }
    }

    static async getMasks(): Promise<any> {
        try {
            const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/dp_views/masks`);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to get masks. Status code: ${error.response?.status}`);
        }
    }
}