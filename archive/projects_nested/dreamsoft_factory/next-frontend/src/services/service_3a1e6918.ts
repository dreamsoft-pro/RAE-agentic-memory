import axios from 'axios';

class PhotoFolderService {
    static async fetchFolders(url: string, sortBy: string, order: string, pagingSettings: { currentPage: number; pageSize: number }, header: Record<string, string>): Promise<any> {
        try {
            const response = await axios.get(
                `${url}folder?sortBy=${sortBy}&order=${order}&page=${pagingSettings.currentPage}&display=${pagingSettings.pageSize}`,
                {
                    headers: header,
                    withCredentials: true
                }
            );
            return response.data;
        } catch (error) {
            throw error.response.status || 500; // Fallback to 500 if status is not available
        }
    }

    static async add(name: string, description: string): Promise<any> {
        try {
            const response = await axios.post(
                `${url}/add`, // Adjust URL as necessary
                { name, description },
                {
                    headers: header,
                    withCredentials: true
                }
            );
            return response.data;
        } catch (error) {
            throw error.response.status || 500; // Fallback to 500 if status is not available
        }
    }
}