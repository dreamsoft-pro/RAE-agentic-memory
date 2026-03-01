import axios from 'axios';
import { Config } from './config'; // Adjust the import based on your project structure

export class SettingService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = Config.API_URL; // Assuming you have a configuration file for API URL
  }

  async getDateByWorkingDays(): Promise<any> {
    try {
      const response = await axios.get(`${this.apiUrl}/settings/getDateByWorkingDays`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error; // Throw the error or response.error based on availability
    }
  }
}