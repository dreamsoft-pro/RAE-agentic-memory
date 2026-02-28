import api from '@/lib/api';
import { rest } from 'next/rest'; // Assuming some import for handling REST operations in Next.js context

export default class CalcFileService {

    private resource: string;

    constructor() {
        this.resource = ['dp_products', 'calcFilesUploader'].join('/');
    }

    public async getUrl(typeID: number): Promise<string> {
        return `${api.API_URL}/${['dp_products', typeID, 'calcFilesUploader'].join('/')}`;
    };

    public async getAllByType(typeID: number): Promise<any[]> {
        const url = await this.getUrl(typeID);
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Failed to get files:', error);
            throw error;
        }
    }

    public async removeFile(typeID: number, fileID: string): Promise<void> {
        const url = `${await this.getUrl(typeID)}/${fileID}`;
        try {
            await fetch(url, { method: 'DELETE' });
        } catch (error) {
            console.error('Failed to delete file:', error);
            throw error;
        }
    }
}