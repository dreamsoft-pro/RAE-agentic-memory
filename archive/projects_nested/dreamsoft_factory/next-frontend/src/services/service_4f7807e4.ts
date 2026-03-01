import api from '@/lib/api';

class ProductCalculator extends React.Component {
    private productAddresses: Array<{ price: string }> | undefined;
    private calculation: { volume?: number } = {};
    private tmpDeliveryPrice: number = 0;
    private netPerPcs: number = 0;

    private async calculateTotalPrice() {
        if (this.productAddresses === undefined) return;

        let totalDeliveryPrice = 0;

        for (let i = 0; i < this.productAddresses.length; i++) {
            const tmp_price = parseFloat(this.productAddresses[i].price.replace(',', '.'));
            totalDeliveryPrice += tmp_price;
        }

        if (this.calculation.volume !== undefined) {
            this.netPerPcs = totalDeliveryPrice / this.calculation.volume;
        }
    }

    // Example usage in a method:
    private async performCalculation() {
        await this.calculateTotalPrice();
        console.log(`Net price per piece: ${this.netPerPcs}`);
    }

    render() {
        return (
            <div>
                {/* Render your component UI here */}
            </div>
        );
    }
}