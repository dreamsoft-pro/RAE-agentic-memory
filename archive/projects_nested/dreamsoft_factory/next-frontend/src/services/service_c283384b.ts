import api from "@/lib/api";

interface ModuleValue {
  id: number;
  name: string;
}

class ModuleValueService {
  private resource = "moduleValues"; // Define resource before use

  constructor(private url: string) {}

  public async getModuleValues(): Promise<ModuleValue[]> {
    try {
      const response = await api.get(`${this.url}/${this.resource}`);
      return response.data as ModuleValue[];
    } catch (error) {
      console.error("Failed to fetch module values", error);
      throw new Error(error.response ? error.response.statusText : "Network Error");
    }
  }

  public async createModuleValue(moduleValue: ModuleValue): Promise<ModuleValue> {
    try {
      const response = await api.post(`${this.url}/${this.resource}`, moduleValue);
      return response.data as ModuleValue;
    } catch (error) {
      console.error("Failed to create module value", error);
      throw new Error(error.response ? error.response.statusText : "Network Error");
    }
  }

  public async updateModuleValue(moduleValue: ModuleValue): Promise<ModuleValue> {
    try {
      const response = await api.put(`${this.url}/${moduleValue.id}`, moduleValue);
      return response.data as ModuleValue;
    } catch (error) {
      console.error("Failed to update module value", error);
      throw new Error(error.response ? error.response.statusText : "Network Error");
    }
  }

  public async deleteModuleValue(id: number): Promise<void> {
    try {
      await api.delete(`${this.url}/${this.resource}/${id}`);
    } catch (error) {
      console.error("Failed to delete module value", error);
      throw new Error(error.response ? error.response.statusText : "Network Error");
    }
  }
}

export default ModuleValueService;