import api from "@/lib/api";

class ProductOrderProcessor {
    async processProductData(data: any, product: any, order: any): Promise<void> {
        const productId = parseInt(product.productID);

        if (data.files[productId] !== undefined) {
            product.fileList = data.files[productId];
            order.filesAlert--;
        } else {
            product.noFiles = true;
        }

        product.reportFiles = [];

        order.acceptCanceled = order.acceptCanceled || product.acceptCanceled;

        if (data.reportFiles && data.reportFiles[productId] !== undefined) {
            product.reportFiles = data.reportFiles[productId];
            order.reportsToAccept += _.reduce(product.reportFiles, function(total: number, n: any) {
                return total + (n.accept === 0 ? 1 : 0);
            }, 0);
        }
    }
}