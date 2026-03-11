import api from "@/lib/api";

class ContentService {
  private resource: string;
  private routeID: string;

  constructor(resource: string, routeID: string) {
    this.resource = resource;
    this.routeID = routeID;
  }

  async update(content: any): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}/${this.resource}/${content.ID}`, content);
      if (response.data.response) {
        cache.remove(this.routeID); // Assuming `cache` is defined elsewhere in your application
        return response.data;
      } else {
        throw new Error('Update failed');
      }
    } catch (error) {
      throw error; // Handle errors as needed
    }
  }

  async remove(content: any): Promise<any> {
    try {
      const response = await api.delete(`${process.env.API_URL}/${this.resource}/${content.ID}`);
      if (response.data.response) {
        cache.remove(this.routeID); // Assuming `cache` is defined elsewhere in your application
        return response.data;
      } else {
        throw new Error('Delete failed');
      }
    } catch (error) {
      throw error; // Handle errors as needed
    }
  }
}

export default ContentService;