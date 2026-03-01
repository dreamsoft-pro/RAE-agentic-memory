import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {

    static addToJoinedDelivery(addressID: string | number, currency: string) {
        return new Promise((resolve, reject) => {
            const params = { addressID, currency };

            axios.patch(`${process.env.API_URL}/${resource}/addToJoinedDelivery`, params)
                .then(response => resolve(response.data))
                .catch(error => reject(error.response ? error.response.data : error));
        });
    }

    static changeAddresses(orderID: string | number, productID: string | number, productAddresses: any[]) {
        return new Promise((resolve, reject) => {
            const params = {
                orderID,
                productID,
                productAddresses
            };

            axios.patch(`${process.env.API_URL}/${resource}/changeAddresses`, params)
                .then(response => resolve(response.data))
                .catch(error => reject(error.response ? error.response.data : error));
        });
    }
}