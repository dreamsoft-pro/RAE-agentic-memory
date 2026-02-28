import api from '@/lib/api';

export default class PsConfigOption {

    private getResource(): string {
        // Implement this method as per your needs.
        return "exampleResource";  // Placeholder implementation.
    }

    async removeIcon(optionID: string): Promise<void> {
        const resource = `${this.getResource()}/uploadIcon`;
        
        try {
            const response = await api.delete(`${resource}/${optionID}`);
            
            if (response.data.response) {
                return;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error: any) {
            throw error;
        }
    }

}