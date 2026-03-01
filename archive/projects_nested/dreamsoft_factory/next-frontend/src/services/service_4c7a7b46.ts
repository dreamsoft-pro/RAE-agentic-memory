import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface ConfigType {
  API_URL: string;
}

class ReclamationService {
  private config: ConfigType;

  constructor(config: ConfigType) {
    this.config = config;
  }

  getFaults = async (): Promise<any> => {
    try {
      const response = await axios.get(`${this.config.API_URL}/dp_reclamation_faults`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  };

  getUploadUrl(reclamationID: string): string {
    return `${this.config.API_URL}/dp_reclamations/files/${reclamationID}`;
  }
}

export default ReclamationService;