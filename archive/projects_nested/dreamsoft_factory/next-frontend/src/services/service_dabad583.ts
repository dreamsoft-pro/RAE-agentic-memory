import api from '@/lib/api';
import { SelectProduct } from '@/types'; // Assuming you have types defined for selectProduct

export default class FormatHandler {
    private selectProduct: SelectProduct;

    constructor(selectProduct: SelectProduct) {
        this.selectProduct = selectProduct;
    }

    async checkCustomFormat(format: any): Promise<void> {
        if (!!format.custom) {
            if (!this.selectProduct.currentFormat?.customWidth) {
                this.selectProduct.currentFormat.customWidth = format.minWidth - (format.slope ?? 0) * 2;
            }
            if (!this.selectProduct.currentFormat?.customHeight) {
                this.selectProduct.currentFormat.customHeight = format.minHeight - (format.slope ?? 0) * 2;
            }
        }

        await this.checkRelatedFormats();
        await this.filterRelatedFormats();

        await this.selectDefaultFormats().then(async () => {
            await this.checkFormatExclusions(this.selectProduct);
            await this.setExclusionsAsync(this.selectProduct);
        });
    }

    private async checkRelatedFormats(): Promise<void> {
        // Implement the logic for checking related formats here
    }

    private async filterRelatedFormats(): Promise<void> {
        // Implement the filtering logic here
    }

    private async selectDefaultFormats(): Promise<void> {
        // Return a resolved promise or implement actual selection logic
        return new Promise((resolve) => resolve());
    }

    private async checkFormatExclusions(selectProduct: SelectProduct): Promise<void> {
        // Logic to check format exclusions. Assume it's an API call here.
        await api.get('/checkFormatExclusions');
    }

    private async setExclusionsAsync(selectProduct: SelectProduct): Promise<void> {
        // Set exclusion logic
        await new Promise((resolve) => setTimeout(() => resolve(), 1000));
    }
}