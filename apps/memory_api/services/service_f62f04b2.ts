import api from '@/lib/api';

class MailTypeService {
  private static async get(resource: string, mailTypeID: number): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${resource}/${mailTypeID}/mailVariables`;
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  }

  private static async create(data: any): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${resource}`;
      const response = await api.post(url, data);
      if (response.data.ID) {
        // Assuming cache.remove is defined elsewhere
        cache.remove('collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  }

  private static update(offer: any): Promise<any> {
    const def = { resolve: (data: any) => data, reject: (reason: any) => reason };
    
    api.put(`${process.env.API_URL}/${resource}`, offer)
      .then((response) => {
        if (response.data.ID) {
          cache.remove('collection');
          return def.resolve(response.data);
        } else {
          return def.reject(response.data);
        }
      })
      .catch((error) => {
        return def.reject(error.response ? error.response.data : error);
      });

    // Return the promise manually constructed
    return new Promise<any>((resolve, reject) => {
      def.resolve = resolve;
      def.reject = reject;
    });
  }

  private static resource: string; // Define required variables as class properties or static members

  public static async getResource(mailTypeID: number): Promise<any> {
    return this.get(this.resource, mailTypeID);
  }

  public static async createResource(data: any): Promise<any> {
    return this.create(data);
  }
}

// Usage
MailTypeService.resource = 'your-resource'; // Set resource to be used in service methods

export default MailTypeService;