import api from "@/lib/api";
import { CreateAsyncThunkOptions } from "@reduxjs/toolkit";

class CalcFileService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    public async cropImage(fileID: string, data: any): Promise<any> {
        try {
            const response = await api.post(`${this.apiUrl}/calcFilesUploader/cropImage/${fileID}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    public async restoreImage(fileID: string): Promise<any> {
        try {
            const response = await api.post(`${this.apiUrl}/calcFilesUploader/restoreImage/${fileID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default CalcFileService;