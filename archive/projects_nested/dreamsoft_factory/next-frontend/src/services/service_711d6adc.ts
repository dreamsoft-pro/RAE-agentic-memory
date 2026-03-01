import api from '@/lib/api';

class MyApiClass {
    private resource: string; // Ensure that 'resource' is defined before use

    constructor() {
        this.resource = ''; // Initialize with an empty string or any default value you need
    }

    public async updateRelativeOptions(optID: number, data: any): Promise<any> {
        const apiUrl = `${process.env.API_URL}/${[this.getResource(), optID, 'relativeOptions'].join('/')}`;

        try {
            const response = await api.put(apiUrl, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response failed');
            }
        } catch (error) {
            throw error; // Re-throw the error to handle it in a higher level
        }
    }

    private getResource(): string {
        // Implement your logic here, or use this.resource if that's all you need
        return this.resource;
    }
}

export default MyApiClass;