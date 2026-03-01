import api from '@/lib/api';

class StatusService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async create(data: any): Promise<any> {
    try {
      const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, data);
      if (response.data.ID) {
        // Simulate cache removal logic
        console.log('Cache removed for collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  public async update(module: any): Promise<any> {
    try {
      const response = await api.put(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, module);
      if (response.data.response) {
        // Simulate cache removal logic
        console.log('Cache removed for collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  public async remove(id: string): Promise<void> {
    try {
      await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${id}`);
      // Simulate cache removal logic
      console.log('Cache removed for specific resource');
    } catch (error) {
      throw error;
    }
  }
}

export default StatusService;

// Usage Example:
// const statusService = new StatusService('yourResourceNameHere');
// statusService.create({ /* data */ });
// statusService.update({ /* module */ });
// statusService.remove('123');