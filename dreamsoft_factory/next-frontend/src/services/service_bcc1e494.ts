import api from "@/lib/api";

class OrderProcessor {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async processOrder(orderData: { total_price: string; delivery_price: string }): Promise<any> {
        const tmpPrice = orderData.total_price;
        const tmpDeliveryPrice = orderData.delivery_price;

        orderData.totalPrice = await this.preparePrice(tmpPrice);
        orderData.totalGrossPrice = await this.preparePrice(tmpPrice);

        orderData.deliveryPrice = await this.preparePrice(tmpDeliveryPrice);
        orderData.deliveryGrossPrice = await this.preparePrice(tmpDeliveryPrice);

        return orderData;
    }

    private async preparePrice(price: string): Promise<string> {
        let tmpPrice = price;

        if (typeof tmpPrice === 'string') {
            tmpPrice = tmpPrice.replace(',', '.');
        }
        tmpPrice = parseFloat(tmpPrice).toFixed(2).replace('.', ',');

        return tmpPrice;
    }

    async getProjects(sort: { [key: string]: string }, pagingSettings?: any): Promise<any> {
        const sortBy = Object.keys(sort)[0];
        const order = sort[sortBy];

        // Assuming $q.defer() is not needed in Next.js/TypeScript, use await here instead.
        try {
            const response = await api.get(this.resource + this.url, { params: { sort_by: sortBy, order: order, ...pagingSettings } });
            return response.data;
        } catch (error) {
            console.error("Failed to get projects:", error);
            throw error; // Rethrow the error or handle it as needed.
        }
    }
}