import api from "@/lib/api";

PsConfigOption.prototype.removeAllPrice = async function (optID: string, priceControllerID: string, priceType: string): Promise<void> {
    const removeResource = [
        this.getResource(),
        optID,
        'priceControllers',
        priceControllerID,
        'ps_prices',
        'removeAll',
        priceType
    ];

    const resource = removeResource.join('/');

    try {
        const response = await api.patch(resource, {});
        if (response.data) {
            return;
        } else {
            throw new Error('Failed to remove prices');
        }
    } catch (error) {
        throw error;
    }
};