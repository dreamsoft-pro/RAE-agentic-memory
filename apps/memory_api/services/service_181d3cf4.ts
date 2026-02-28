import api from '@/lib/api';

class CalculationHandler {
    private orderID: string | undefined;
    private userID: string | undefined;

    constructor(private savedCalculation: any, private product: any) {}

    public async handleSavedCalculation(): Promise<void> {
        if (this.savedCalculation.orderID) {
            this.orderID = this.savedCalculation.orderID;
        }

        this.savedCalculation.volume = this.product.preparedProduct.volume;

        await this.copyAddressesToNewProduct();

        if (this.userID !== undefined) {
            this.savedCalculation.userID = this.userID;
        }
    }

    private async copyAddressesToNewProduct(): Promise<void> {
        const data = await new Promise((resolve, reject) => {
            // Assuming copyAddressesToNewProduct is an API call or a function that returns a promise
            api.copyAddressesToNewProduct(this.product).then(resolve).catch(reject);
        });

        if (this.orderID !== undefined && this.userID === undefined) {
            throw new Error('userID must be defined before setting in savedCalculation.');
        }

        // Here you may want to handle data or do something with it, but the example does not require it.
    }
}