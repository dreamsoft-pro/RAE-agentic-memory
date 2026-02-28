import api from "@/lib/api";

class EditorProjectService {
    static async shareMyProject(email: string, projectID: string): Promise<any> {
        const resource = 'projects';
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${projectID}/share`;
        const headers = { /* your headers here */ };
        
        try {
            const response = await api.post(url, { emails: [email] }, { headers });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to share project with error: ${error.message}`);
        }
    }

    static async shareMyProjectByFb(projectID: string): Promise<any> {
        const resource = 'projects';
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${projectID}/share/fb`;
        const headers = { /* your headers here */ };
        
        try {
            const response = await api.post(url, {}, { headers });
            return response.data;
        } catch (error) {
            throw new Error(`Failed to share project via FB with error: ${error.message}`);
        }
    }
}

export default EditorProjectService;