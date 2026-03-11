import api from '@/lib/api';

class TemplateService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getFile(templateID: number): Promise<string> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/getFile/${templateID}`;
        return url; // This would typically involve making an API call, but for now it just returns the URL.
    }

    public async uploadFile(template: { ID: number; file: File }): Promise<void> {
        const formData = new FormData();
        formData.append('file', template.file);
        formData.append('templateID', String(template.ID));

        try {
            await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/upload/${template.ID}`, formData, { headers: { 'Content-Type': 'multipart/form-data' } });
        } catch (error) {
            console.error(error);
        }
    }

    public async remove(templateID: number): Promise<void> {
        try {
            await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${templateID}`);
        } catch (error) {
            throw error;
        }
    }
}

export default TemplateService;