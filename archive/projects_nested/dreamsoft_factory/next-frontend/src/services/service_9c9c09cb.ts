import axios from 'axios';

export default class PhotoFolderService {
    private static instance: PhotoFolderService;

    private baseUrl: string;
    private headers: Record<string, string>;

    private constructor(baseUrl: string, headers: Record<string, string>) {
        this.baseUrl = baseUrl;
        this.headers = headers;
    }

    public static getInstance(baseUrl: string, headers: Record<string, string>): PhotoFolderService {
        if (!PhotoFolderService.instance) {
            PhotoFolderService.instance = new PhotoFolderService(baseUrl, headers);
        }
        return PhotoFolderService.instance;
    }

    private async sendRequest<T>(url: string, method: 'POST' | 'GET', data?: any): Promise<T> {
        try {
            const response = await axios({
                url: this.baseUrl + url,
                method,
                headers: { ...this.headers },
                data,
                withCredentials: true
            });
            return response.data;
        } catch (error) {
            throw new Error(`Request failed with status ${error.response?.status}`);
        }
    }

    public async addPeoplesToImage(imageID: string, data: any): Promise<any> {
        const url = `add-peoples-to-image/${imageID}`;
        return this.sendRequest(url, 'POST', data);
    }

    public async getImageByExtension(id: string, extension: string): Promise<Blob> {
        const url = `get-image-in-extension/${id}/${extension}`;
        return this.sendRequest(url, 'GET');
    }
}