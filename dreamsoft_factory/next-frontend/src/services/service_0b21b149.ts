import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    // Assuming getResource() returns this.resource and is defined elsewhere in the class.
    public async getEfficiency(optID: string, controllerID: string): Promise<any> {
        if (!this.resource) throw new Error('Resource must be defined before calling getEfficiency');
        
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.getResource(), optID, 'efficiency', controllerID].join('/')}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    private getResource(): string {
        // Implement this method to return the resource.
        return this.resource;  // This should be replaced with actual logic
    }
}

export default PsConfigOption;