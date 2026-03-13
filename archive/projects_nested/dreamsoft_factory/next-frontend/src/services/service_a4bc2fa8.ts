import api from '@/lib/api';

class PsConfigOption {
    private getResource(): string {
        // Placeholder for actual resource retrieval logic
        return 'configOptions';
    }

    public async patchSortOptions(sortList: any): Promise<void> {
        const resource = this.getResource();
        try {
            const response = await api.patch(`${resource}/sortOptions`, sortList);
            if (response.data.response === true) {
                return;
            }
            throw new Error('Failed to update sort options');
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    public async getRealizationTimes(optID: string): Promise<any[]> {
        const resource = `${this.getResource()}/${optID}/optionRealizationTimes`;
        try {
            const response = await api.get(resource);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    public async addRealizationTime(optID: string, item: any): Promise<void> {
        const resource = `${this.getResource()}/${optID}/optionRealizationTimes`;
        try {
            await api.post(resource, item);
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

export default PsConfigOption;