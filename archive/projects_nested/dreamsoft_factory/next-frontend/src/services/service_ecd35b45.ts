import api from "@/lib/api";

class PrintTypeService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  getResource(): string {
    return this.resource;
  }

  async remove(item: { ID: number | string }) {
    try {
      const response = await api.delete(`${this.getResource()}/${item.ID}`);
      cache.remove(this.resource);
      return response.data;
    } catch (error) {
      throw new Error(error.response ? error.message : JSON.stringify(error));
    }
  }

  async devices(printtype: { ID: number | string }) {
    try {
      const url = `${api.defaults.baseURL}/${this.getResource()}/${printtype.ID}/ps_printtypeDevices`;
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw new Error(JSON.stringify(error));
    }
  }

  async setDevices(printtype: { ID: number | string }, devices: any[]) {
    try {
      const url = `${api.defaults.baseURL}/${this.getResource()}/${printtype.ID}/ps_printtypeDevices`;
      const response = await api.put(url, devices);
      return response.data;
    } catch (error) {
      throw new Error(JSON.stringify(error));
    }
  }
}

export default PrintTypeService;

// Usage:
const printTypeService = new PrintTypeService('your-resource-name');