import api from '@/lib/api';

class CalcFileService {
  private apiUrl: string = '/calcFilesUploader'; // Assuming a base API URL

  async editImage(fileID: number | string, data: any): Promise<any> {
    const url = `${this.apiUrl}/editImage/${fileID}`;
    try {
      const response = await api.post(url, data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export default CalcFileService;