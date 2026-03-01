import api from "@/lib/api";

export default class EditorProjectService {
    private url: string;
    private header: any;

    constructor(url: string, header: any) {
        this.url = url;
        this.header = header;
    }

    async getProjectsData(projects: any): Promise<any> {
        try {
            const response = await api.post(this.url + '/getProjectsData', { projects }, { headers: this.header, withCredentials: true });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch data. Status code: ${error.response?.status}`);
        }
    }
}