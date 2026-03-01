import axios from 'axios';
import { useEffect, useState } from 'react';

export default class PhotoFolderService {

    static async savePhoto(photoId: string, fileData: string, thumbSize: number, minSize: number, mainSize: number) {
        try {
            const response = await axios.post(
                `${url}userUploadEdited/projectImage`,
                {
                    image64: fileData,
                    projectImage: photoId,
                    thumbSize: thumbSize,
                    minSize: minSize,
                    mainSize: mainSize
                },
                {
                    headers: header,
                    withCredentials: true
                }
            );
            return response.data;
        } catch (error) {
            throw new Error(`Request failed with status: ${error.response?.status}`);
        }
    }

    static async addTag(imageID: string, tag: string) {
        try {
            // Implement the actual logic for adding a tag here
            const response = await axios.post(
                `${url}tagEndpoint`, // Replace with actual endpoint
                {
                    imageId: imageID,
                    tag: tag
                },
                {
                    headers: header,
                    withCredentials: true
                }
            );
            return response.data;
        } catch (error) {
            throw new Error(`Request failed with status: ${error.response?.status}`);
        }
    }
}