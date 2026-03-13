import api from '@/lib/api';

class PsConfigOption {
    private getResource(): string {
        // Implement this method as needed.
        return 'your-resource-name';
    }

    public async doPOST(item: any): Promise<any> {
        const resource = `${this.getResource()}`;
        try {
            const data = await api.post(resource, item);
            if (data.ID) {
                return data;
            } else {
                throw new Error('Failed to post with ID');
            }
        } catch (error) {
            throw error;
        }
    }

    public async removeRealizationTime(optID: string, item: any): Promise<any> {
        const resource = `${this.getResource()}/${optID}/optionRealizationTimes`;
        try {
            const data = await api.delete(`${resource}/${item.ID}`);
            if (data.response) {
                return data;
            } else {
                throw new Error('Failed to delete');
            }
        } catch (error) {
            throw error;
        }
    }
}

export default PsConfigOption;