import api from '@/lib/api';

class DepartmentService {
  private resource: string;
  private apiUrl: string;

  constructor(resource: string) {
    this.resource = resource;
    this.apiUrl = process.env.API_URL; // Assuming API_URL is set in environment variables
  }

  public async delete(id: number): Promise<any> {
    try {
      const response = await api.delete(`${this.apiUrl}/${this.resource}/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error(error);
    }
  }

  public async sort(sortData: any): Promise<any> {
    try {
      const response = await api.patch(`${this.apiUrl}/${this.resource}/sort`, { data: sortData });
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error(error);
    }
  }

  static sort(sort: any) {
    // Static method, can be called without creating an instance
    const departmentService = new DepartmentService('department'); // Example resource name
    return departmentService.sort(sort);
  }
}

export default DepartmentService;