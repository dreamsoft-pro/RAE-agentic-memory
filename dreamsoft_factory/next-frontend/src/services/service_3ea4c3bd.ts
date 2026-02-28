import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface ConfigType {
  API_URL: string;
}

class DpCategoryService {
  private config: ConfigType;

  constructor(config: ConfigType) {
    this.config = config;
  }

  public async getContains(categoryUrl: string): Promise<any> {
    try {
      const response = await axios.get(`${this.config.API_URL}/dp_categories/getContains/${categoryUrl}`);
      return response.data;
    } catch (error) {
      console.log(error);
      throw error;
    }
  }

  public forView(): Promise<void | any> {
    const def = new Promise((resolve, reject) => {
      // Implement your logic here
      resolve();
    });
    return def;
  }
}

export default DpCategoryService;