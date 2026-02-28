import api from '@/lib/api';

class CalculationService {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async getCalculationData(): Promise<void> {
        try {
            const response = await api.get(this.url);
            const calculation = response.data;

            if (calculation.volume !== undefined) {
                calculation.gross_per_pcs = calculation.price / calculation.volume;
            }

            let tmpPriceTotal: number | string | undefined;
            if (calculation.priceTotalBrutto !== undefined) {
                if (typeof calculation.priceTotalBrutto === 'string') {
                    tmpPriceTotal = parseFloat(calculation.priceTotalBrutto.replace(',', '.'));
                } else {
                    tmpPriceTotal = calculation.priceTotalBrutto;
                }
            }

            // You can now use `tmpPriceTotal` as needed within your service logic
        } catch (error) {
            console.error('Failed to fetch calculation data:', error);
        }
    }
}