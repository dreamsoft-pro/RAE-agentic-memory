import api from '@/lib/api';

class CalcFileService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    public async setImageSepia(fileID: number): Promise<any> {
        try {
            const response = await api.post(this.getUrl('setImageSepia', fileID));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async setCollectionToBW(setID: number): Promise<any> {
        try {
            const response = await api.post(this.getUrl('setCollectionToBW', setID));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    private getUrl(methodName: string, id: number): string {
        return `${this.apiUrl}/${['calcFilesUploader', methodName, id].join('/')}`;
    }
}