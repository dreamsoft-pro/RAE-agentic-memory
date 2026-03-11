import api from '@/lib/api';

class ComplexProductPageController {
    private selectedProduct: any;
    private currentPages: number;

    constructor(selectedProduct: any, currentPage?: number) {
        this.selectedProduct = selectedProduct;
        if (currentPage !== undefined) {
            this.currentPages = currentPage;
        } else {
            this.currentPages = Number(this.selectedProduct.data?.currentPages ?? 0);
        }
    }

    public selectPages(pages: number): void {
        if (!this.selectedProduct.data?.pages || !Array.isArray(this.selectedProduct.data.pages)) return;

        const firstPageItem = this.selectedProduct.data.pages[0];
        if (firstPageItem && Array.isArray(firstPageItem.pages)) {
            this.currentPages = pages;
        }
    }

    public getSelectedProductData(): any {
        return this.selectedProduct.data;
    }

    public getCurrentPages(): number {
        return this.currentPages;
    }
}

// Usage example
const selectedProduct: any = { data: { currentPages: '42', pages: [{ pages: [1, 2] }] } };
const controller = new ComplexProductPageController(selectedProduct);
controller.selectPages(50);
console.log(controller.getCurrentPages()); // Output should be 50 if conditions are met