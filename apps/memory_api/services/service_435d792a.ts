import api from "@/lib/api";
import { globalParams, getPagingSettings } from "@/utils";

interface CommonData {
    deliveries: any[];
    addresses: any[];
    senders: any[];
    count?: number;
    orders: any[];
}

class DeliveryService {

    private async getCommonData(): Promise<CommonData> {
        let commonData = {} as CommonData;

        try {
            const deliveries = await api.getDeliveries();
            commonData.deliveries = deliveries;

            const addressResponse = await api.getAddress();
            commonData.addresses = addressResponse.addresses;
            commonData.senders = addressResponse.senders;

            let params: any = {};
            params = { ...params, ...globalParams };

            const counted = await api.countOrders(params);
            if (counted.count > 0) {
                commonData.count = counted.count;
            }

            params.limit = getPagingSettings().pageSize;
            params.offset = 0;

            const ordersData = await api.getOrders(statuses, params);

            ordersData.forEach(singleOrder => {
                const dateOnly = singleOrder.created.split(' ')[0];
                const date = dateOnly.split('-');
                singleOrder.simpleCreateDate = `${date[2]}-${date[1]}-${date[0]}`;
            });

            commonData.orders = ordersData;

        } catch (error) {
            console.error("Error fetching data: ", error);
        }

        return commonData;
    }
}

// Example usage of the class:
const deliveryService = new DeliveryService();
deliveryService.getCommonData().then(commonData => {
    // Handle resolved commonData here
});