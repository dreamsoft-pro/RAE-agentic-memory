import api from "@/lib/api";

class ProductHandler {
    async handleProductPages(product: { pages: Array<{ step?: number }> }, currentPage: number): Promise<number> {
        const resource = product.pages[0];
        if (resource.step !== null) {
            const urlParams = new URLSearchParams(window.location.search);
            let pages = parseInt(urlParams.get('page') || '1', 10);
            
            if (pages % resource.step !== 0) {
                if ((pages % resource.step) > (resource.step / 2)) {
                    pages += (resource.step - (pages % resource.step));
                } else {
                    pages -= pages % resource.step;
                }
            }

            return pages;
        }

        throw new Error("Step value is null or missing");
    }
}