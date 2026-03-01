import api from "@/lib/api";

class PsConfigAttribute {
    static getUploadUrl(): string {
        const resource = getResource();
        resource.push('uploadIcon');
        return `${process.env.NEXT_PUBLIC_API_URL}/${resource.join('/')}`;
    }

    static async deleteIcon(categoryID: string): Promise<any> {
        try {
            const resource = getResource();
            resource.push('uploadIcon');
            resource.push(categoryID);

            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${resource.join('/')}`);
            
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(response.statusText);
            }
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

function getResource(): string[] {
    // Implement the logic to get resource array
    return ['path', 'to', 'resource'];
}

export default PsConfigAttribute;