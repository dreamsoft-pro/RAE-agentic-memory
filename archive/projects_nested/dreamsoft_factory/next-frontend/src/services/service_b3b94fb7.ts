import api from '@/lib/api';

class AddressService {
  private async updateProductAddresses(orderID: string, productID: string, productAddresses: any[]): Promise<any> {
    const params = {
      orderID,
      productID,
      productAddresses
    };

    try {
      const response = await api.post(`${process.env.AUTH_URL}/product/addresses`, { domainName: location.hostname }, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        },
        data: new URLSearchParams(params).toString()
      });

      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  }

  public static getSingleton(): AddressService {
    if (!AddressService.instance) {
      AddressService.instance = new AddressService();
    }
    return AddressService.instance;
  }

  private constructor() {}

  // Public method to be used
  public async performUpdate(orderID: string, productID: string, productAddresses: any[]): Promise<any> {
    try {
      const data = await this.updateProductAddresses(orderID, productID, productAddresses);
      return data;
    } catch (error) {
      throw error;
    }
  }
}

export default AddressService;

// Usage example
const addressServiceInstance = AddressService.getSingleton();
addressServiceInstance.performUpdate('order123', 'product456', [{ /* product addresses */ }])
  .then(data => console.log(data))
  .catch(error => console.error(error));