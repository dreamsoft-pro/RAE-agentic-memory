import axios, { AxiosResponse } from 'axios';
import { getCartData } from './path-to-get-cart-data'; // Adjust the path as necessary

class AddressService {
  static async updateProductAddresses(orderID: string, productID: string, addresses: any[]): Promise<AxiosResponse> {
    return await axios.put(`/api/update-product-addresses/${orderID}/${productID}`, { addresses });
  }
}

class DpCartsDataService {
  static async update(patchData: { orderID: string; productID: string; productAddresses: any[] }): Promise<AxiosResponse> {
    return await axios.patch('/api/patch-cart', patchData);
  }
}

const updateCartProduct = async (product: { orderID: string; productID: string; addresses: any[] }) => {
  try {
    const savedData = await AddressService.updateProductAddresses(product.orderID, product.productID, product.addresses);

    if (savedData.data.response === true) {
      const patchData = {
        orderID: product.orderID,
        productID: product.productID,
        productAddresses: product.addresses
      };

      const patchResponse = await DpCartsDataService.update(patchData);

      if (patchResponse.data.response === true) {
        getCartData();
      } else {
        Notification.error('error'); // Ensure Notification and error message are properly imported or defined
      }
    } else {
      Notification.error('error'); // Ensure Notification and error message are properly imported or defined
    }
  } catch (error) {
    console.error(error);
    Notification.error('error'); // Ensure Notification and error message are properly imported or defined
  }
};