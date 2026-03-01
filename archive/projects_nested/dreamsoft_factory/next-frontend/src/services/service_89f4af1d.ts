import api from '@/lib/api';

class EditorProjectService {
    static async getSharedProjectFromFB(projectID: string, url: string, header: any): Promise<any> {
        try {
            const response = await api.post(url + ['getsharedProjectFromFB', projectID].join('/'), {}, { headers: header });
            return response.data;
        } catch (error) {
            throw new Error(`Request failed with status code ${error.response.status}`);
        }
    }

    static async getProjectsData(projects: any[]): Promise<any[]> {
        const promises = projects.map(project => this.getSharedProjectFromFB(project.projectID, project.url, project.header));
        return await Promise.all(promises);
    }
}