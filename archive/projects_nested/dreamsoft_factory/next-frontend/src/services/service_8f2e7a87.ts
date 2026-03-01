import api from '@/lib/api';
import { useState } from 'react';

class ViewService {
  private getResource(): string {
    // Implement the logic to get the resource as per your application's requirement.
    return ''; 
  }

  public async addVariable(data: any, viewID: string): Promise<any> {
    const url = `${api.API_URL}/${this.getResource()}/variables`;
    try {
      const response = await api.post(url, data);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Response error');
      }
    } catch (error) {
      throw error;
    }
  }

  public async addViewTemplate(data: any): Promise<any> {
    const url = `${api.API_URL}/${this.getResource()}`;
    try {
      const response = await api.post(url, data);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export default ViewService;