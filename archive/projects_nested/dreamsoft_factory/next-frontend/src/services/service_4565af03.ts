import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface Config {
  API_URL: string;
}

class ComplexService {
  private config: Config;

  constructor(config: Config) {
    this.config = config;
  }

  getResource(): string {
    // Implement your logic to return the resource
    return '';
  }

  getRelatedFormat(baseFormatID: number): Promise<any> {
    const url = `${this.config.API_URL}/${[this.getResource(), 'relatedFormat', baseFormatID].join('/')}`;
    
    return axios.get(url).then(response => response.data)
               .catch(error => { throw error; });
  }

  saveRelatedFormat(baseFormatID: number, formats: any[]): Promise<any> {
    const url = `${this.config.API_URL}/${[this.getResource()].join('/')}`;

    return axios.post(url, { baseFormatID, formats })
               .then(response => response.data)
               .catch(error => { throw error; });
  }
}