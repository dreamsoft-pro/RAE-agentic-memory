import api from "@/lib/api";

class ContentService {
  resource: string; // Ensure this is defined somewhere in your class

  async create(content) {
    try {
      const response = await api.post(this.resource, content);
      if (response.data.response) {
        cache.remove(this.routeID); // Make sure `cache` and `routeID` are properly defined
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error; // or handle the error as needed
    }
  }

  async edit(content) {
    try {
      content.action = "edit";
      const response = await api.post(this.resource, content);
      if (response.data.response) {
        cache.remove(this.routeID); // Make sure `cache` and `routeID` are properly defined
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error; // or handle the error as needed
    }
  }
}