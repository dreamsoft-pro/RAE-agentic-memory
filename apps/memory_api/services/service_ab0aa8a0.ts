import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class PhotoFolderService {
    static movePhoto(url: string, header: object, data: any, photo: any, fromFolderID: string) {
        return new Promise((resolve, reject) => {
            axios.post(
                url + 'folder/photo/move/' + photo._id,
                { targetFolder: data.selectedFolder._id, from: fromFolderID },
                { headers: header, withCredentials: true }
            ).then(response => resolve(response.data))
             .catch(error => reject(error.response ? error.response.status : null));
        });
    }

    static copyPhoto(data: any, photo: any) {
        // Implement the copy photo logic here.
        // Since the original code snippet does not include implementation details for copyPhoto,
        // you need to provide a proper implementation based on your requirements.
        return new Promise((resolve, reject) => {
            // Example placeholder:
            axios.post(
                'your-copy-url', 
                { /* data */ }, 
                { headers: {/* headers */}, withCredentials: true }
            ).then(response => resolve(response.data))
             .catch(error => reject(error.response ? error.response.status : null));
        });
    }
}

export default PhotoFolderService;