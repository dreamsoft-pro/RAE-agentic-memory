import api from "@/lib/api";

class StaticPrice {
  resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  async set(item: any): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}/${this.resource}`, item);
      cache.remove(this.resource); // Remove the cached data
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error("Failed to set resource");
    }
  }

  async remove(id: string): Promise<any> {
    try {
      const response = await api.delete(`${process.env.API_URL}/${this.resource}/${id}`);
      cache.remove(this.resource); // Remove the cached data
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error("Failed to remove resource");
    }
  }
}