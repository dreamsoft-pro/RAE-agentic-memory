import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL; // Assuming you have set this in your environment variables

class StaticContentService {
  private resource: string[];

  constructor() {
    this.resource = this.getResource();
  }

  private getResource(): string[] {
    return ['dp_static_contents'];
  }

  public async getContent(key: string): Promise<any> {
    try {
      const response = await axios.get(`${API_URL}/${this.resource.join('/')}/getContent/${key}`);
      return response.data;
    } catch (error) {
      console.log(error);
      throw error; // You can handle errors here if needed
    }
  }
}

export default StaticContentService;