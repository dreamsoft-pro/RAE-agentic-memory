import api from '@/lib/api';

export default class PsConfigOption {
    private getResource(): string {
        // Assuming this method exists and returns the resource path.
        return 'someResourcePath';
    }

    public async removeDiscountPrice(optID: string, controllerID: string, item: { ID: number }, discountGroupID?: string): Promise<any> {
        const resource = `${this.getResource()}/${optID}/priceControllers/${controllerID}/ps_prices`;

        try {
            const response = await api.patch(resource, { remove: item.ID, discountGroupID });
            if (response.response) {
                return response;
            } else {
                throw new Error('Response is not valid');
            }
        } catch (error) {
            throw error;
        }
    }
}