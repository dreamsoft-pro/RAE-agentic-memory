import api from '@/lib/api';

class VariableController {
    private getResource(): string {
        // Mock implementation for demonstration purposes
        return 'example-resource';
    }

    async deleteVariable(variableID: number): Promise<any> {
        const resource = this.getResource();
        
        try {
            const response = await api.delete(`${resource}/variables/${variableID}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid data received');
            }
        } catch (error: any) {
            throw error;
        }
    }

    // Add other methods here
}

export default VariableController;