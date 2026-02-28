import axios from 'axios';
import { AxiosResponse } from 'axios';

class PhotoFolderService {

    static updatePhotoLocation(photoId: string, position: any, header: any): Promise<AxiosResponse> {
        return axios.post(`${url}folder/photo-location/${photoId}`, { location: position }, { headers: header, withCredentials: true });
    }

    static getAll(sort: {[key: string]: number}, pagingSettings: any): Promise<AxiosResponse> {
        const sortBy = Object.keys(sort)[0];
        const order = Object.values(sort)[0];

        console.log(sortBy, order);

        // Add your logic to handle the request here
        return axios.get(`${url}folder/photos`, { params: { sort_by: sortBy, order }, headers: {} }); // Example GET request. Adjust as necessary.
    }
}