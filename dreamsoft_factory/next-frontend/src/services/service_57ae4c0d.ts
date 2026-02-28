import api from '@/lib/api';

class TemplateService {

    static async removeFile(template: { ID: number; own?: boolean }) {
        let root = 0;
        if (template.own === false) {
            root = 1;
        }
        const data = { templateID: template.ID, root };

        try {
            const response = await api.post([resource, 'removeFile'].join('/'), data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(String(error));
        }
    }

}

export default TemplateService;

// Ensure the variable `resource` is defined before using it
const resource = 'your-resource-name-here'; // Replace with actual value

// Usage example:
TemplateService.removeFile({ ID: 123, own: false })
    .then(data => console.log('Success:', data))
    .catch(error => console.error('Error:', error));