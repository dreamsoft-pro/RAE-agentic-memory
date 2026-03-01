import api from '@/lib/api';

class CalcFileService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    public async copyImage(fileID: number): Promise<any> {
        try {
            const response = await api.post(this.getCopyImageUrl(fileID));
            return response.data;
        } catch (error) {
            throw error.response?.data ?? error;
        }
    }

    public async changeQty(fileID: number, data: any): Promise<any> {
        try {
            const response = await api.patch(this.getChangeQtyUrl(fileID), data);
            return response.data;
        } catch (error) {
            throw error.response?.data ?? error;
        }
    }

    private getCopyImageUrl(fileID: number): string {
        return `${this.apiUrl}/calcFilesUploader/copyImage/${fileID}`;
    }

    private getChangeQtyUrl(fileID: number): string {
        return `${this.apiUrl}/calcFilesUploader/changeQty/${fileID}`;
    }
}