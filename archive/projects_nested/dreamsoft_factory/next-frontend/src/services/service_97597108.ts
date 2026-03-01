import axios from 'axios';

class PhotoFolderService {
    static async create(folder: { _id: string; folderName: string; description: string }): Promise<any> {
        return await axios.post(url + 'folder/', {
            folderId: folder._id,
            folderName: folder.folderName,
            description: folder.description
        }, {
            headers: header,
            crossDomain: true
        });
    }

    static async delete(folder: { _id: string }): Promise<any> {
        return await axios.delete(url + 'folder/', {
            data: { folderId: folder._id },
            headers: header,
            crossDomain: true
        });
    }

    static getPhotos(folderId: string, sort?: any, pagingSettings?: any): Promise<any> {
        // Implement the GET request logic here
        return axios.get(url + 'photos/', {
            params: { folderId, sort, ...pagingSettings },
            headers: header,
            crossDomain: true
        });
    }
}