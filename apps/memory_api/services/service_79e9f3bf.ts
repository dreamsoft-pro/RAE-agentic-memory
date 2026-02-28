import axios from 'axios';

class PhotoFolderService {
    private static instance: PhotoFolderService;

    private constructor(private url: string, private header: Record<string, string>) {}

    public static getInstance(url: string, header: Record<string, string>): PhotoFolderService {
        if (!PhotoFolderService.instance) {
            PhotoFolderService.instance = new PhotoFolderService(url, header);
        }
        return PhotoFolderService.instance;
    }

    public addTag(imageID: number | string, tag: string): Promise<any> {
        return axios.post(`${this.url}folder/image-tag/${imageID}/${tag}`, {}, { headers: this.header, withCredentials: true })
            .then(response => response.data)
            .catch(error => Promise.reject(error.response?.status || error.message));
    }

    public removeTag(imageID: number | string, tag: string): Promise<any> {
        return axios.post(`${this.url}folder/delete-image-tag/${imageID}/${tag}`, {}, { headers: this.header, withCredentials: true })
            .then(response => response.data)
            .catch(error => Promise.reject(error.response?.status || error.message));
    }
}

// Usage example:
const photoFolderService = PhotoFolderService.getInstance('your-api-url', { 'Content-Type': 'application/json' });
photoFolderService.addTag(1, 'tagname')
    .then(data => console.log(data))
    .catch(status => console.error(`Request failed with status ${status}`));