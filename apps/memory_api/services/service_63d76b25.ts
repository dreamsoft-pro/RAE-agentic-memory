import api from '@/lib/api';

class TooltipService {
    private resource: string = 'your-resource'; // Replace with actual resource name

    public async save(attrID: number, tooltips: any): Promise<any> {
        try {
            const response = await api.patch(this.resource, { attrID, tooltip: tooltips });
            if (response.response) {
                cache.remove(this.resource); // Assuming cache is defined elsewhere
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error;
        }
    }
}

// Usage example:
const service = new TooltipService();
service.save(123, { tooltipText: 'This is a tooltip' })
    .then(data => console.log('Saved successfully:', data))
    .catch(error => console.error('Failed to save:', error));

export default TooltipService;