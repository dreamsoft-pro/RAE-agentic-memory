import api from '@/lib/api';

class OperationService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async fetchOperation(id: number): Promise<void> {
    try {
      const url = `/api/${this.resource}/${id}`;
      const response = await api.get(url);
      console.log('Response:', response.data); // You may need to adapt the handling of data
    } catch (error) {
      console.error(`Error fetching operation for ${id}:`, error);
    }
  }

  public async createOperation(operation: any): Promise<void> {
    try {
      const url = `/api/${this.resource}`;
      await api.post(url, operation);
      console.log('Operation created successfully');
    } catch (error) {
      console.error(`Error creating operation:`, error);
    }
  }

  // Add other methods as needed
}

export default OperationService;