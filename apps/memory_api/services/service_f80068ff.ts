import axios from 'axios';

class PhotoFolderService {

    static async vote(folderId: string, vote: string): Promise<void> {
        try {
            await axios.post(url + `folder/${folderId}/vote/${vote}`, {}, { headers: header, withCredentials: true });
        } catch (error) {
            throw error.response.status;
        }
    }

    static async votePhoto(photoId: string, vote: string): Promise<void> {
        try {
            await axios.post(url + `folder/image-vote/${photoId}/${vote}`, {}, { headers: header, withCredentials: true });
        } catch (error) {
            throw error.response.status;
        }
    }
}