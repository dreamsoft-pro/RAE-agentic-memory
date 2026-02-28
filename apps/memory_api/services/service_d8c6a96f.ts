import api from '@/lib/api';

class ViewService {
  private getResource(): string {
    // Implement this method based on your requirements.
    return 'your-resource';
  }

  public async editResource(data: any): Promise<any> {
    const resource = this.getResource();
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;

    try {
      const response = await api.put(url, data);
      console.log(response.data);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error: any) {
      throw error;
    }
  }

  public async editVariable(data: any): Promise<any> {
    const resource = this.getResource();
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/variables`;

    try {
      const response = await api.put(url, data);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error: any) {
      throw error;
    }
  }

  public async removeVariable(variableID: string): Promise<any> {
    const resource = this.getResource();
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/variables/${variableID}`;

    try {
      await api.delete(url);
      // Handle success or add specific logic if needed.
    } catch (error: any) {
      throw error;
    }
  }
}