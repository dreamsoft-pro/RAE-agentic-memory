import axios from 'axios';
import qs from 'qs';

class PhotoFolderService {
    static async getPhotos(url: string, folderId: string, sort: {[key: string]: any}, pagingSettings: { currentPage: number; pageSize: number }, header: object): Promise<any> {
        const sortBy = Object.keys(sort)[0];
        const order = Object.values(sort)[0];

        try {
            const response = await axios.get(url + 'folder/' + folderId, {
                params: {
                    sortBy,
                    order,
                    page: pagingSettings.currentPage,
                    display: pagingSettings.pageSize
                },
                headers: header,
                paramsSerializer: (params) => qs.stringify(params)
            });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.status : 'Unknown Error';
        }
    }

    static async deletePhoto(url: string, folderId: string, photoId: string, header: object): Promise<void> {
        try {
            await axios.delete(`${url}folder/${folderId}/photo/${photoId}`, { headers: header });
        } catch (error) {
            throw error.response ? error.response.status : 'Unknown Error';
        }
    }
}