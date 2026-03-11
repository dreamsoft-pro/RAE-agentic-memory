import api from "@/lib/api";

class ProductService {
    async deleteProduct(scope: any, product: any): Promise<boolean> {
        try {
            const data = await api.DpProductService.delete(product);

            if (data.response === true) {
                if (product.inEditor) {
                    await api.DpProductService.deleteFromMongo(product);
                }
                
                scope.$emit('cartRequired');
                return true;
            } else {
                throw new Error("Deletion failed");
            }
        } catch (err) {
            throw err;
        }
    }
}