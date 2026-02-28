import api from "@/lib/api";

class AdminHelpService {

  private resource: string;

  constructor() {
    this.resource = 'help'; // Example value, should be set appropriately based on actual usage context.
  }

  getKeys(moduleName: string): Promise<any> {
    return api.get(`${this.resource}/${moduleName}/helpKeys`).then(response => response.data)
      .catch(error => { throw error; });
  }

  addKey(moduleName: string, key: any): Promise<any> {
    return api.post(`${this.resource}/${moduleName}/helpKeys`, key).then(response => {
      if (response.data.response) {
        return response.data.item;
      } else {
        throw new Error('Failed to add key');
      }
    }).catch(error => { throw error; });
  }

  editKey(moduleName: string, key: any): Promise<any> {
    const def = this.defer();
    
    api.put(`${this.resource}/${moduleName}/helpKeys/${key.id}`, key).then(response => {
      if (response.data.response) {
        def.resolve(response.data.item);
      } else {
        def.reject(new Error('Failed to edit key'));
      }
    }).catch(error => {
      def.reject(error);
    });

    return def.promise;
  }

  private defer(): { resolve: (value?: any) => void; reject: (reason?: any) => void } {
    let resolveFunc, rejectFunc;

    const promise = new Promise((resolve, reject) => {
      resolveFunc = resolve;
      rejectFunc = reject;
    });

    return { resolve: resolveFunc!, reject: rejectFunc! };
  }
}

export default AdminHelpService;