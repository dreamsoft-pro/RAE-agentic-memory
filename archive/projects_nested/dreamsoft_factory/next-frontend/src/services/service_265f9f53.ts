import api from "@/lib/api";
import DpOrderService from "@/services/DpOrderService"; // Assuming the service is imported like this
import PaymentService from "@/services/PaymentService"; // Assuming the service is imported like this

class OrdersClass {
    private ordersData: any[] = [];

    async fetchOrders(): Promise<void> {
        const ordersResponse = await api.get('/orders');
        this.ordersData = ordersResponse.data;
    }

    async getPayments(orderID?: string): Promise<any[]> {
        return PaymentService.getAll().then(data => data);
    }

    async payment(params: any, orderID: string): Promise<any> {
        return DpOrderService.payment(params, orderID).then(data => data);
    }

    addDeliveryToOrder(order: { products: any[] }) {
        if (!order.deliveryPrice) order.deliveryPrice = 0;
        if (!order.deliveryGrossPrice) order.deliveryGrossPrice = 0;

        _.each(order.products, (product) => {
            // Logic to update delivery price based on product
        });
    }

    return this.ordersData; // This line doesn't fit in a class method. Consider moving the logic elsewhere.
}