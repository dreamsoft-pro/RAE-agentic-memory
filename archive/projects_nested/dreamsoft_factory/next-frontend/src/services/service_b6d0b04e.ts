import api from '@/lib/api';
import { NextApiRequest, NextApiResponse } from 'next';

export default class UploadService {
    static async upload(uploader: any, formData: FormData): Promise<any> {
        let dataResolve: (value?: any) => void;

        const promise = new Promise((resolve, reject) => {
            dataResolve = resolve;
            
            uploader.onSuccessItem = function (item: any, data: any) {
                dataResolve(data);
            };
        
            const file = uploader.queue[0];
            if (!file) throw new Error('File not found in queue');

            uploader.data = {};
            file.formData = [formData];

            try {
                await api.post('/upload', formData); // Assuming this triggers the upload
                uploader.uploadItem(file);
            } catch (error) {
                reject(error);
            }
        });

        return promise;
    }

    static async handleRequest(req: NextApiRequest, res: NextApiResponse) {
        const { uploader, formData } = req.body;

        try {
            const result = await this.upload(uploader, formData);
            res.status(200).json(result);
        } catch (error) {
            res.status(500).send(error.message || 'An unexpected error occurred');
        }
    }
}