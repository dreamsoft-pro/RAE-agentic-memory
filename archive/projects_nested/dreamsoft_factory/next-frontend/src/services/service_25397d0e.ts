import api from '@/lib/api';

class PsConfigOption {
    private getResource(): string {
        // Implement this method according to your needs.
        throw new Error('getResource not implemented');
    }

    public async patchRemove(itemID: number): Promise<any> {
        const resource = `${this.getResource()}/${itemID}/remove`;

        try {
            const response = await api.patch(resource, { remove: itemID });
            return response;
        } catch (error) {
            throw error;
        }
    }

    public async countIncreases(optID: number): Promise<any> {
        const resource = `${this.getResource()}/${optID}/ps_countIncreases`;

        try {
            const response = await api.get(resource);
            return response.data.plain();
        } catch (error) {
            throw error;
        }
    }

    public async countPrices(optID: number): Promise<any> {
        const resource = `${this.getResource()}/${optID}/ps_countPrices`;

        // Implement the rest of this method according to your needs.
        throw new Error('countPrices not implemented');
    }
}

export default PsConfigOption;